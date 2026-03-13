import websockets
import logging
import json
import asyncio
from .. import error
from ..command_related.commands import Commands

class WebsocketHandler:
    gateway_url = "wss://gateway.discord.gg/?v=10&encoding=json"

    def __init__(self, commandbus):
        self.logger = logging.getLogger(__name__)
        self.emit = commandbus.emit
        self.reset_running = False
        self.ws = None

    async def reset(self):
        if self.reset_running is True:
            return 22
        
        self.reset_running = True

        error_handling = error.HandleGatewayErrors()

        while True:
            try:
                await self.emit(Commands.STOP_LISTENER)
                await self.emit(Commands.STOP_HB_WATCHDOG)
                await self.emit(Commands.STOP_HB_LOOP)

                self.logger.debug("Attempting to connect to websocket.")

                self.ws = await websockets.connect(self.gateway_url, ping_interval=None, ping_timeout=None, open_timeout=5)

                self.logger.debug(f"Websocket connected successfully.")

                self.reset_running = False
                await self.emit(Commands.START_LISTENER, fire_and_forget=True)
                return
            
            except Exception as e:
                self.logger.warning("Reset attempt failed trying again.")
                await error_handling.handle_gateway_errors(self.ws, e)
                continue

    async def send_websocket_message(self, data):
        self.logger.debug(f"Sending websocket message {data}")
        try:
            await self.ws.send(json.dumps(data))

        except Exception as e:
            self.logger.error(f"Connection closed while trying to send a message. Code {self.ws.close_code}. Attempting to restart. {e}")
            await self.emit(Commands.CLIENT_RESET_NEEDED, fire_and_forget=True)
            await asyncio.Future() # Will be cancelled shortly

    async def receive_message(self):
        self.logger.debug("Waiting for message...")
        try:
            msg = await self.ws.recv()

        except Exception as e:
            self.logger.error(f"Connection closed while trying to receive message. Code {self.ws.close_code}. Attempting to restart. {e}")
            await self.emit(Commands.CLIENT_RESET_NEEDED, fire_and_forget=True)
            await asyncio.Future() # Will be cancelled shortly

        if type(msg) is str:
            return json.loads(msg)
        
        elif type(msg) is bytes:
            self.logger.critical("Received BYTES from DISCORD. This should not have happened.")
            raise RuntimeError()