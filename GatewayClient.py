import websockets
import asyncio
import json
import GatewayClientErrors

class Bot():
    def __init__(self, username=None, id=None, discriminator=None, session_id=None, payload=None):
        self.username = username
        self.id = id
        self.discriminator = discriminator
        self.session_id = session_id
        self.payload = payload

class DiscordGatewayClient():
    discord_gateway = "wss://gateway.discord.gg/?v=10&encoding=json"

    def __init__(self, TOKEN=None, callback=None, intents=None):
        if callback is None:
            raise GatewayClientErrors.UnassingedCallbackFunctionError("You have to assign a callback function to use the DiscordGatewayClient class.")
        
        if TOKEN is None:
            raise GatewayClientErrors.InvalidTokenError("You need to provide your Discord token.")
        
        if intents is None:
            raise GatewayClientErrors.InvalidBotIntents("You need to provide a valid discord intent!")
        
        self.TOKEN = TOKEN
        self.callback = callback
        self.intents = intents

        self.discord_should_send_ready = False
        self.bot = None
        self.sequence = None
        self.sequence_lock = asyncio.Lock()
        self.heartbeat_ready = asyncio.Event()

    async def _save_sequence(self, sequence):
        async with self.sequence_lock:
            self.sequence = sequence

    async def _get_sequence(self):
        async with self.sequence_lock:
            return self.sequence

    async def _identify(self):
        try:
            payload  = {
                "op": 2, # IDENTIFY
                "d": {
                    "token": self.TOKEN,
                    "intents": self.intents,
                    "properties": {
                        "os": "Windows",
                        "browser": "Fireoncrack",
                        "device": "Windows"
                    }
                }
            }
            await self.ws.send(json.dumps(payload))

            self.discord_should_send_ready = True

        except websockets.exceptions.ConnectionClosed as e:
            await self._handle_websocket_errors(e)
            return

    async def _send_data(self, type, data=None):
        await self.callback(self, type, data)
    
    async def _reset(self):
        try:
            if hasattr(self, "watch_dog"):
                self.watch_dog.cancel()

            if hasattr(self, "start_sending_heartbeat"):
                self.start_sending_heartbeat.cancel()

            if hasattr(self, "ws"):
                await self.ws.close()

            self.heartbeat_ready.clear()

            self.ws = await websockets.connect(self.discord_gateway)

        except websockets.exceptions.ConnectionClosed as e:
            await self._handle_websocket_errors(e)
        except OSError as e:
            await self._handle_connection_errors(e)

    async def _resume(self):
        try:
            if not hasattr(self.bot, "session_id"):
                raise RuntimeError("session_id is empty. Why was _resume() called?")
            
            await self._reset()
            
            payload = {
                "op": 6, # Attempt to RESUME
                "d": {
                    "token": self.TOKEN,
                    "session_id": self.bot.session_id,
                    "seq": await self._get_sequence()
                }
            }

            await self.ws.send(json.dumps(payload))

            asyncio.create_task(self._heartbeat(response_json=None, resuming=True))
            
            await self.heartbeat_ready.wait()

            self.watch_dog = asyncio.create_task(self._is_connection_dead())

        except websockets.ConnectionClosed as e:
            await self._handle_websocket_errors(e)
            return

    async def _is_connection_dead(self):
        try:
            await asyncio.sleep(self.heartbeat_interval * 1.1)
            await self._reset()
        except asyncio.CancelledError:
            return
        except websockets.exceptions.ConnectionClosed as e:
            await self._handle_websocket_errors(e)
        
    async def _send_heartbeat_loop(self):
        while True:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                payload = {"op": 1, "d": await self._get_sequence()}
                await self.ws.send(json.dumps(payload))
                asyncio.create_task(self._send_data(type="Sent HEARTBEAT"))
            except asyncio.CancelledError:
                return
            except websockets.exceptions.ConnectionClosed as e:
                await self._handle_websocket_errors(e)
    
    async def _heartbeat(self, response_json, resuming=False):
        try:
            if resuming is False:
                self.heartbeat_interval = response_json['d']['heartbeat_interval'] / 1000
                    
            self.start_sending_heartbeat = asyncio.create_task(self._send_heartbeat_loop())

            self.heartbeat_ready.set()

        except websockets.exceptions.ConnectionClosed as e:
            await self._handle_websocket_errors(e)
            return
        
    async def _handle_responses(self):
        while True:
            try:
                response = await self.ws.recv() 
                response_json = json.loads(response)
                response_code = response_json['op']
                response_event = response_json.get('t', None)

                if response_code == 1:
                    payload = {"op": 1, "d": await self._get_sequence()}
                    await self.ws.send(json.dumps(payload))
                    asyncio.create_task(self._send_data(type="Sent HEARTBEAT"))

                elif response_code == 10 or response_code == 9: # HELLO / INVALID_SESSION
                    if response_code == 9:
                        await self._reset()
                        asyncio.create_task(self._send_data(type="INVALID_SESSION"))

                    await self._identify()
                    asyncio.create_task(self._heartbeat(response_json))
                    await self.heartbeat_ready.wait()
                    self.watch_dog = asyncio.create_task(self._is_connection_dead())
                    continue

                elif response_code == 11: # Heartbeat ACK
                    asyncio.create_task(self._send_data(type="Received Heartbeat ACK"))
                    self.watch_dog.cancel()
                    self.watch_dog = asyncio.create_task(self._is_connection_dead())
                    continue

                elif response_code == 7: # RECONNECT
                    await self._resume()
                    asyncio.create_task(self._send_data(type="RECONNECT"))
                    continue

                elif response_code == 0: # DISPATCH / Discord sending an event
                    await self._handle_events(response_event, response_json)
                    
                else:
                    asyncio.create_task(self._send_data(type=response_code, data=response_json))
                    continue

            except websockets.ConnectionClosed as e:
                await self._handle_websocket_errors(e)

    async def _handle_events(self, response_event, response_json):
            try:
                if response_json.get('s') is not None:
                    await self._save_sequence(sequence=response_json['s'])

                if self.discord_should_send_ready is True:
                    if response_event == "READY":
                        self.bot = Bot()
                        self.bot.session_id = response_json['d']['session_id']
                        self.bot.username = response_json['d']['user']['username']
                        self.bot.id = response_json['d']['user']['id']
                        self.bot.discriminator = response_json.get('d').get('user').get('discriminator')
                        self.bot.payload = response_json
                        asyncio.create_task(self._send_data(type="READY"))
                        self.discord_should_send_ready = False
                        return
                    else:
                        raise RuntimeError(f"Discord responded with something other than READY to IDENTIFY.\nDiscord responded with these things:\n\nThe event: {response_event}\nThe raw json:\n\n\n\n{response_json}")
                    
                elif response_event == "RATE_LIMITED":
                    asyncio.create_task(self._send_data(type=response_event, data=response_json))
                    sleep = response_json['d']['timeout'] / 1000
                    await asyncio.sleep(sleep)
                else:
                    asyncio.create_task(self._send_data(type=response_event, data=response_json))
                    return
            except websockets.ConnectionClosed as e:
                await self._handle_websocket_errors(e)

    async def _handle_websocket_errors(self, e):
        if e.code == 4004: # Invalid Token
            await self.ws.close()
            raise GatewayClientErrors.InvalidTokenError(f"Invalid Token! Token that is invalid: {self.TOKEN}")
        elif e.code == 1000: # Normal Close
            await self._reset()
            return
        elif e.code == 1006: # Wifi Disconnected or server down
            raise GatewayClientErrors.ServerDownError("Connection abruptly lost. Server down or no wifi?")
        elif e.code == 4001: # Unknown OP sent
            await self._reset()
            print("UNKNOWN OP CODE SENT!")
            return
        elif e.code == 4002: # Decode Error
            await self._reset()
            print("MALFORMED JSON (invalid payload) SENT.")
        elif e.code == 4003:
            raise GatewayClientErrors.InvalidTokenError("Invalid Token!")
        elif e.code == 4005: # Already Authenticated
            return
        elif e.code == 4007: # Tried to RESUME with an invalid sequence
            await self._reset()
            return
        elif e.code == 4009: # Session timed out
            await self._reset()
            return
        elif e.code == 5000: # Unknown server error
            await self._reset()
            return
        elif e.code == 5001: # Invalid Gateway Version
            await self.ws.close()
            raise RuntimeError("Invalid Gateway Version")
        elif e.code == 5002: # Invalid Intents
            await self.ws.close()
            raise GatewayClientErrors.InvalidBotIntents(f"Invalid bot Intents: {self.intents}")
        else:
            raise GatewayClientErrors.UnhandledClosedConnectionCodeError(f"Unhandled Error Code: {e.code}\n\nFull traceback:\n\n\n\n{e}")

    async def _handle_connection_errors(self, e):
        if e.errno == 11001: # Could not fetch address I.e, website down or no internet
            raise GatewayClientErrors.ServerDownError("Could not fetch server address. Server down or no wifi?")
        else:
            raise(e)

    async def start(self):
        try:
            self.ws = await websockets.connect(self.discord_gateway)
            await self._handle_responses()
        except OSError as e:
            await self._handle_connection_errors(e)
        except websockets.exceptions.ConnectionClosed as e:
            await self._handle_websocket_errors(e)

if __name__ == "__main__":
    raise RuntimeError("This program is not intended to be ran independently.")