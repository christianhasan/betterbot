import logging
from ..command_related.commands import Commands
import asyncio

class HeartbeatService:
    def __init__(self, commandbus, session):
        self.logger = logging.getLogger(__name__)

        self.emit = commandbus.emit
        self.session = session
        self.watchdog = None
        self.heartbeat_loop = None
        self.payload = {"op": 1, "d": session.sequence}

    async def _start_heartbeat_watchdog(self):
        try:
            self.logger.debug("Started heartbeat watchdog.")
            await asyncio.sleep(self.session.heartbeat_interval * 1.5)
            self.logger.warning("I AM BARKING I AM BARKING! DOG ALERT. Watchdog triggered. Discord didn't respond with Heartbeat ACK.")
            await self.emit(Commands.CLIENT_RESET_NEEDED, fire_and_forget=True) # Fire amd forget needed for safety
        
        except asyncio.CancelledError: pass

    async def _loop_send_heartbeat(self):
        self.logger.debug(f"Heartbeat loop started with heartbeat interval of {self.session.heartbeat_interval}")
        while True:
            await asyncio.sleep(self.session.heartbeat_interval)
            asyncio.create_task(self.send_heartbeat())

    async def stop_hb_watchdog(self):
        if isinstance(self.watchdog, asyncio.Task) and not self.watchdog.done():
            self.watchdog.cancel()
            self.logger.debug("Heartbeat watchdog stopped.")

    async def stop_hb_loop(self):
        if isinstance(self.heartbeat_loop, asyncio.Task) and not self.heartbeat_loop.done():
            self.heartbeat_loop.cancel()
            self.logger.debug("Heartbeat loop stopped.")

    async def start_hb_watchdog(self):            
        await self.stop_hb_watchdog()
        self.watchdog = asyncio.create_task(self._start_heartbeat_watchdog())

    async def start_hb_loop(self):
        await self.stop_hb_loop()
        self.heartbeat_loop = asyncio.create_task(self._loop_send_heartbeat())

    async def send_heartbeat(self):
        await self.emit(Commands.SEND_WEBSOCKET_MESSAGE, fire_and_forget=True, data=self.payload)
        self.logger.debug("Sent a heartbeat")