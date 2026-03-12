import logging
import asyncio
from ..command_related.commands import Commands

class HandleResponses:
    def __init__(self, commandbus, session):
        self.emit = commandbus.emit
        self.session = session
        self.logger = logging.getLogger(__name__)
        self.listener = None

    async def _listener(self):
        try:
            self.logger.debug("Listener started")
            while True:
                message = await self.emit(Commands.RECEIVE_WEBSOCKET_MESSAGE)
                if not message:
                    continue
                asyncio.create_task(self.handle_responses(message))
                self.logger.debug(f"Received a message and sent it to handle_responses.")
                
        except asyncio.CancelledError:
            self.logger.debug("Listener Cancelled.")

    async def stop_listener(self):
        if isinstance(self.listener, asyncio.Task) and not self.listener.done():
            self.listener.cancel()

    async def start_listener(self):
        await self.stop_listener()
        self.listener = asyncio.create_task(self._listener())

    async def handle_responses(self, message):
        response_json = message
        response_code = response_json["op"]
        response_data = response_json.get("d", None)

        if response_code == 1: # Send heartbeat NOW!
            await self.emit(Commands.SEND_ONE_HEARTBEAT)
    
        elif response_code == 10: # HELLO
            self.session.heartbeat_interval = response_data["heartbeat_interval"] / 1000
            await self.emit(Commands.IDENTIFY_NEEDED)
            await self.emit(Commands.START_HB_LOOP, fire_and_forget=True)
            await self.emit(Commands.START_HB_WATCHDOG, fire_and_forget=True)

        elif response_code == 9: # Invalid Session
            await self.emit(Commands.CLIENT_RESET_NEEDED)

        elif response_code == 11:
            await self.emit(Commands.RESTART_HB_WATCHDOG)

        elif response_code == 0:
            await self.emit(Commands.HANDLE_EVENT, fire_and_forget=True, response_json=response_json)