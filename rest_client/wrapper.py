import httpx
import asyncio
import logging
import time
import json
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
        self.global_lock = asyncio.Lock()
        self.write_lock = asyncio.Lock()
        self.cache_count = 0
        self.buckets = {}
        self.identifiers = {}

        self._load_cache()

    def _load_cache(self):
        amount = 604800 # One week

        try:
            with open(".__betterbot_cache__.json", "r") as f:
                cache = json.load(f)

                if time.time() - cache["time"] > amount:
                    self.logger.info("Cache is too old. A new cache file will be created.")
                else:
                    for bucket_id, bucket in cache["buckets"].items():
                        bucket["x-ratelimit-limit"] = -1
                        bucket["x-ratelimit-remaining"] = -1
                        bucket["x-ratelimit-reset"] = 0

                        bucket["lock"] = asyncio.Lock()

                    self.buckets = cache["buckets"]
                    self.identifiers = cache["identifiers"]

        except FileNotFoundError:
            self.logger.info("No cache found")
        except json.JSONDecodeError:
            self.logger.error("Cache file invalid.")
        except PermissionError:
            self.logger.error("Permission ERROR: Cannot read cache")
        except KeyError:
            self.logger.error("Cache content not expected.")

            self.identifiers = None
            self.buckets = None

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

            sleep = info.get("retry_after", 1)
            global_limit = info.get("global", False)

            if global_limit is True:
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
        self.cache_count += 1
        bucket = response.headers.get("x-ratelimit-bucket", None) 
        limit = int(response.headers.get("x-ratelimit-limit", -1))
        remaining = int(response.headers.get("x-ratelimit-remaining", -1))
        reset = float(response.headers.get("x-ratelimit-reset", 0))
        
        self.logger.debug(f"Bucket response from discord is {bucket}")
        self.logger.debug(f"x-rate-limit response from discord is {limit}")
        self.logger.debug(f"remaining response from discord is {remaining}")
        self.logger.debug(f"Reset unix time response from discord is {reset} and current time in unix is {time.time()}")

        if bucket in self.buckets and identifier not in self.identifiers:
            self.logger.debug(f"New identifier for existing bucket: {bucket}. The new identifier is {identifier}")
            self.identifiers[identifier] = bucket

        elif identifier in self.identifiers and bucket not in self.identifiers.values():
            async with self.write_lock:
                if identifier in self.identifiers and bucket not in self.identifiers.values():
                    self.logger.debug(f"Discord updated their bucket for {identifier} new_bucket: {bucket}")
                    del self.identifiers[identifier]
            
        if bucket is not None and bucket not in self.buckets and identifier not in self.identifiers:
            self.logger.debug(f"Saving a bucket as {bucket}")
            self.buckets[bucket] = {"lock": asyncio.Lock()}
            self.identifiers[identifier] = bucket

        if self.buckets.get(bucket):
            self.logger.debug("New x-rate-limit from discord updating existing.")
            to_update = self.buckets[bucket]
            to_update.update({
                "x-ratelimit-limit": limit,
                "x-ratelimit-remaining": remaining, 
                "x-ratelimit-reset": reset
                })

        if self.cache_count == 25: # Caches every 25 times.
            async with self.write_lock:
                if self.cache_count == 25: # Caches every 25 times.
                    self.cache_count = 0
                    with open(".__betterbot_cache__.json", "w") as f:
                        write_buckets = {key: {k: v for k,v in value.items() if k != "lock"}
                        for key, value in self.buckets.items()
                        }

                        to_cache = {"buckets": write_buckets, "identifiers": self.identifiers, "time": time.time()}
                        json.dump(to_cache, f, indent=2)

    async def _request(self, method, endpoint, identifier, json=None):
        connection = 0
        while True:
            try:
                if json:
                    self.logger.info(f"A json is sent the json is: {json}")

                await self.global_rate_limit.wait()

                response = await self.http.request(method, endpoint, headers={"Authorization": f"Bot {self.token}"}, json=json)

                content_type = response.headers.get("Content-Type", None)

                await self._handle_bucket(identifier, response)
                what_to_do = await self._status_codes(response)

                if what_to_do == ResponseTypes.SUCCESS:
                    self.logger.info("Successfully completed your request")
                    if "application/json" in content_type and response.json() is not None:
                        response_json = response.json()
                        return response_json
                    else:
                        return ResponseTypes.SUCCESS
                                        
                elif what_to_do == ResponseTypes.FAILED:
                    self.logger.warning(f"Your attempt to send a request failed. Code {response.status_code}")
                    return ResponseTypes.FAILED
                
                elif what_to_do == ResponseTypes.RETRY_DELAY:
                    await asyncio.sleep(connection*3)
                    connection += 1
                    if connection == 5:
                        return ResponseTypes.CONNECTION_FAILED
                    continue

                elif what_to_do == ResponseTypes.RETRY_NOW:
                    continue

            except (OSError,httpx.ConnectError, gaierror, httpx.ReadTimeout):
                    self.logger.error(f"Your attempt to send a request failed. Is the network or server down?")
                    return ResponseTypes.CONNECTION_FAILED

    async def request(self, method, endpoint, identifier, json=None):    
        async def send_identifier():
            bucket = self.identifiers[identifier]
            bucket_in_buckets = self.buckets[bucket]
            lock = bucket_in_buckets["lock"]

            async with lock:
                reset_time = bucket_in_buckets["x-ratelimit-reset"]
                current_time = time.time()

                self.logger.debug(f"Existing identifier for this bucket: {bucket}")

                self.logger.debug(f"From self.request() Current unix time is {current_time} and reset time is {reset_time}")

                if bucket_in_buckets["x-ratelimit-remaining"] == 0 and reset_time - current_time > 0:
                    sleep_time = reset_time - current_time
                    self.logger.warning(f"Throttling requests to send as discord requests it. Sleeping for the requested amount: {sleep_time}")
                    
                    await asyncio.sleep(sleep_time)
                            
                return await self._request(method, endpoint, identifier, json)

        if identifier in self.identifiers:
            return await send_identifier()
        
        else:
            await self.global_lock.acquire()
            if identifier in self.identifiers:
                self.global_lock.release()
                return await send_identifier()
            
            response = await self._request(method, endpoint, identifier, json)
            self.global_lock.release()
            return response
