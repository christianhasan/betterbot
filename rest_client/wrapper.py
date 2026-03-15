import httpx
import asyncio
import logging
import time
from socket import gaierror
from . import error
from ..enums import ResponseTypes

class HttpWrapper:
    def __init__(self, token):
        self.logger = logging.getLogger(__name__)
        self.token = token
        self.global_rate_limit = asyncio.Event()
        self.global_rate_limit.set()
        self.http = httpx.AsyncClient(timeout=20)
        self.lock = asyncio.Lock()
        self.buckets = {}
        self.heartbeat = {}
        self.identifiers = {}
        self.listener_watchdogs = {}
        self.listeners = {} # A reference is required to avoid GC and for other logic

    async def _listener(self, queue, bucket):
        try:
            self.logger.debug("Started a listener")
            while True:
                task = await queue.get()
                self.logger.debug("Found something in queue")
                self.heartbeat[bucket] = time.time()
                await task
                queue.task_done()
        except asyncio.CancelledError: pass

    async def _listener_heartbeat(self, bucket):
        while True:
            await asyncio.sleep(1000)
            difference = time.time() - self.heartbeat[bucket]
            if difference > 950:
                self.logger.debug("Killing inactive listener")
                self.listeners[bucket].cancel()
                return
                
    async def _start_listener(self, bucket, queue):
        task = self.listeners.get(bucket, None)

        if task is None or task.done():
            self.logger.debug("No listeners for this bucket starting new task")
            self.heartbeat[bucket] = time.time()
            self.listeners[bucket] = asyncio.create_task(self._listener(queue, bucket))
            if bucket not in self.listener_watchdogs:
                self.listener_watchdogs[bucket] = asyncio.create_task(self._listener_heartbeat(bucket))
        else:
            self.logger.debug("Existing listeners for this bucket found.")

    async def _status_codes(self, response):
        status_code = response.status_code
        self.logger.debug(f"The status code response is {status_code}")

        if status_code == 401:
            raise error.InvalidTokenError("Invalid token!")

        elif status_code in [200, 201, 202, 203, 204, 304]:
            return ResponseTypes.SUCCESS
    
        elif status_code in [403, 404, 400, 405]:
            return ResponseTypes.FAILED
        
        elif status_code in [500, 502, 504]:
            return ResponseTypes.RETRY_DELAY
        
        elif status_code == 429:
            info = response.json()
            sleep = info["retry_after"]
            if info["global"] is True:
                self.logger.warning(f"GLOBAL LIMIT REACHED! Sleeping for {sleep}")
                self.global_rate_limit.clear()
                await asyncio.sleep(sleep)
                self.global_rate_limit.set()
            else:
                self.logger.info(f"Discord rate-limiting. Sleeping for: {sleep}")
                await asyncio.sleep(sleep)

            return ResponseTypes.RETRY_NOW
        
        else:
            self.logger.critical("Unhandled Status code treating as unsuccessful.")
            return ResponseTypes.FAILED

    async def _handle_bucket(self, identifier, response):
        bucket = response.headers.get("x-ratelimit-bucket", None) 
        limit = int(response.headers.get("x-ratelimit-limit", -1))
        remaining = int(response.headers.get("x-ratelimit-remaining", -1))
        reset_after = float(response.headers.get("x-ratelimit-reset-after", 0))
        
        self.logger.debug(f"Bucket response from discord is {bucket}")
        self.logger.debug(f"x-rate-limit response from discord is {limit}")
        self.logger.debug(f"remaining response from discord is {remaining}")
        self.logger.debug(f"Reset after response from discord is {reset_after}")

        if bucket in self.buckets and identifier not in self.identifiers:
            self.logger.debug(f"New identifier for existing bucket: {bucket}. The new identifier is {identifier}")
            self.identifiers.update({identifier: bucket})

        elif identifier in self.identifiers and bucket not in self.identifiers.values():
            async with self.lock:
                if identifier in self.identifiers and bucket not in self.identifiers.values():
                    old_bucket = self.identifiers[identifier]
                    self.logger.debug(f"Discord updated their bucket for {identifier}  old_bucket: {old_bucket}  new_bucket: {bucket}")
                    del self.buckets[old_bucket]
                    del self.identifiers[identifier]
            
        elif bucket is not None and bucket not in self.buckets and identifier not in self.identifiers:
            self.logger.debug(f"Saving a bucket as {bucket}")
            self.buckets[bucket] = {"queue": asyncio.Queue()}
            self.identifiers.update({identifier: bucket})

        if self.buckets.get(bucket):
            self.logger.debug("New x-rate-limit from discord updating existing.")
            to_update = self.buckets[bucket]
            to_update.update({
                "x-ratelimit-limit": limit,
                "x-ratelimit-remaining": remaining, 
                "x-ratelimit-reset-after": reset_after
                })

    async def _request(self, method, endpoint, identifier, future, json=None, is_in_queue=None):
        connection = 0
        while True:
            try:
                if json is not None:
                    self.logger.debug("A json is sent the json is: ")
                await self.global_rate_limit.wait()
                response = await self.http.request(method, endpoint, headers={"Authorization": f"Bot {self.token}"}, json=json)

                content_type = response.headers.get("Content-Type", None)

                await self._handle_bucket(identifier, response)
                what_to_do = await self._status_codes(response)

                if what_to_do == ResponseTypes.SUCCESS:
                    self.logger.info("Successfully completed your request")
                    if "application/json" in content_type and response.json() is not None:
                        response_json = response.json()
                        self.logger.debug(f"The response is a json and is {response_json}")
                        future.set_result(response_json)
                        return response_json
                    else:
                        future.set_result(ResponseTypes.SUCCESS)
                        return ResponseTypes.SUCCESS
                                        
                elif what_to_do == ResponseTypes.FAILED:
                    self.logger.warning(f"Your attempt to send a request failed. Code {response.status_code}")
                    future.set_result(ResponseTypes.FAILED)
                    return ResponseTypes.FAILED
                
                elif what_to_do == ResponseTypes.RETRY_DELAY:
                    await asyncio.sleep(connection*3)
                    connection += 1
                    if connection == 5:
                        return ResponseTypes.CONNECTION_FAILED
                    continue

                elif what_to_do == ResponseTypes.RETRY_NOW:
                    if is_in_queue is False:
                        bucket = self.identifiers[identifier]
                        bucket_in_buckets = self.buckets[bucket]

                        await bucket_in_buckets["queue"].put(self._request(method, endpoint, identifier, future, json, is_in_queue=True))
                        await self._start_listener(bucket, bucket_in_buckets["queue"])
                        return
                    else:
                        continue

            except (OSError,httpx.ConnectError, gaierror, httpx.ReadTimeout):
                    self.logger.error(f"Your attempt to send a request failed. Is the network or server down?")
                    future.set_result(ResponseTypes.CONNECTION_FAILED)

    async def request(self, method, endpoint, identifier, json=None):
        future = asyncio.Future()
    
        if identifier in self.identifiers:
            bucket = self.identifiers[identifier]
            bucket_in_buckets = self.buckets[bucket]
            self.logger.debug(f"Existing identifier for this bucket: {bucket}")

            if bucket_in_buckets["x-ratelimit-remaining"] == 0:
                sleep = bucket_in_buckets["x-ratelimit-reset-after"]
                self.logger.info(f"Throttling requests to send. Sleeping for this much: {sleep}")
                await asyncio.sleep(sleep)
            
            await bucket_in_buckets["queue"].put(self._request(method, endpoint, identifier, future, json, is_in_queue=True))

            await self._start_listener(bucket, bucket_in_buckets["queue"])

            return await future
        else:
            return await self._request(method, endpoint, identifier, future, json, is_in_queue=False)