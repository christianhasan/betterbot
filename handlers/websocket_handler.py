import aiohttp
import logging
import asyncio
from .. import error
from ..event_related.commands import Commands

class WebsocketHandler:
    gateway_url = "wss://gateway.discord.gg/?v=9&encoding=json"

    def __init__(self, commandbus):
        self.logger = logging.getLogger(__name__)
        self.emit = commandbus.emit
        self.reset_counter = 0
        self.keep_retrying_forever = False
        self.reset_lock = asyncio.Lock()
        self.reset_running = False
        self.ws = "closed"

    async def _gateway_errors(self):
        if self.ws.close_code == 1000:
            self.logger.warning("Discord closed for maintainence or related. Close code 1000. Script will keep trying forever.")
            self.keep_retrying_forever = True

        elif self.ws.close_code == 4001:
            self.logger.error("Please report this. Unknown opcode was sent.")

        elif self.ws.close_code == 4003:
            self.logger.critical("Discord responded with NOT_AUTHENTICATED code 4003. This should be impossible. Report this please.")

        elif self.ws.close_code == 4004:
            raise error.InvalidTokenError("Token is invalid. Code 4004")
        
        elif self.ws.close_code == 4005:
            self.logger.error("Discord responded with ALREADY_AUTHENTICATED. This shouldn't happen. Code 4005")

        elif self.ws.close_code == 4008:
            self.logger.warning("Discord is ratelimiting gateway connect attempts. Sleeping for ten seconds before retry. Code 4008")
            await asyncio.sleep(10)

        elif self.ws.close_code == 4013:
            raise error.InvalidIntentsError("Invalid Intents. Code 4013")
        
        elif self.ws.close_code == 4014:
            raise error.DisallowedIntentsError("You must open discord developer portal and enable intents. Code 4014.")

    async def ws_connect(self):
        self.session = aiohttp.ClientSession()

        await self.reset(setup=True)

        return self.session, self.ws

    async def reset(self, setup=False):
        if self.reset_running is True:
            return
        
        self.reset_running = True

        while True:
            try:
                await self.emit(Commands.STOP_LISTENER)
                await self.emit(Commands.STOP_HB_WATCHDOG)
                await self.emit(Commands.STOP_HB_LOOP)

                if not hasattr(self.ws, "closed") and setup is False:
                    await self.ws.close()
                
                self.ws = await self.session.ws_connect(self.gateway_url)

                if self.ws.closed:
                    await self._gateway_errors()
                    continue

                self.logger.debug(f"Websocket connected successfully.")

                self.reset_counter = 0
                self.keep_retrying_forever = False
                await self.emit(Commands.START_LISTENER, ws=self)
                self.reset_running = False
                return self.ws

            except Exception as e:
                self.logger.error(f"An error has happened while trying to reset. Will try to reset again for a maximum of 20 times. ERROR: {e}")
                self.reset_counter += 1
                
                if self.reset_counter == 20 and self.keep_retrying_forever is False:
                    raise error.MaxRetiresAttempted("Multiple retries attempted and failed.")

                elif self.reset_counter >= 3 and self.reset_counter <= 10:
                    await asyncio.sleep(5)

                if self.reset_counter >= 10:
                    await asyncio.sleep(15)

                continue
                
    async def send_websocket_message(self, data):
        self.logger.debug(f"Sending websocket message {data}")
        try:
            await self.ws.send_json(data)

            if self.ws.closed:
                self.logger.error(f"An error has happened while trying to send a message attempting restart. Code: {self.ws.close_code}")
                await self.reset()

        except Exception as e:
            self.logger.error(f"An error has happened while trying to send a message attempting restart. ERROR: {e}")
            await self.reset()

    async def receive_message(self):
        self.logger.debug("Waiting for message...")
        try:
            msg = await self.ws.receive()
            self.logger.debug(f"Received this message from recieve: {msg}")

            if self.ws.closed:
                self.logger.error(f"An error has happened while trying to receive a message attempting restart. Code: {self.ws.close_code}")
                await self.reset()

            elif msg.type == aiohttp.WSMsgType.TEXT:
                return msg.json()
            elif msg.type == aiohttp.WSMsgType.BINARY:
                pass # Not implemented

        except Exception as e:
            self.logger.error(f"An error has happened while trying to receive a message attempting restart. ERROR: {e}")
            await self.reset()