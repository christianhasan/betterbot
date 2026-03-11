from .handlers.websocket_handler import WebsocketHandler
from .command_related.commandbus import Commandbus
from . import error
from .command_related.commands import Commands
from .connection.identify import Identify
from .connection.heartbeatservice import HeartbeatService
from .connection.session import Session
from .event_related.eventbus import EventBus
from .handlers.handle_responses import HandleResponses
from .handlers.handle_event_responses import HandleEventResponses
import asyncio
import logging

class Setup:
    def __init__(self, token):
        if token is None:
            raise error.InvalidTokenError("You must provide your discord token.")
        
        self.token = token
        self.event = EventBus()
        self.stop = asyncio.Event()

    def _start_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="log.txt",
            filemode="w",
        )

    async def start(self):
        self._start_logging()

        commandbus = Commandbus()
        session = Session()
        session.token = self.token

        websocket_handler = WebsocketHandler(commandbus)
        handle_events = HandleEventResponses(self.event, session)
        identify = Identify(commandbus, session)
        heartbeat_service = HeartbeatService(commandbus, session)
        handle_responses = HandleResponses(commandbus, session)

        await commandbus.register(Commands.IDENTIFY_NEEDED, identify.identify)

        await commandbus.register(Commands.CLIENT_RESET_NEEDED, websocket_handler.reset)
        await commandbus.register(Commands.SEND_WEBSOCKET_MESSAGE, websocket_handler.send_websocket_message)
        await commandbus.register(Commands.RECEIVE_WEBSOCKET_MESSAGE, websocket_handler.receive_message)

        await commandbus.register(Commands.RESTART_HB_WATCHDOG, heartbeat_service.start_hb_watchdog)
        await commandbus.register(Commands.START_HB_WATCHDOG, heartbeat_service.start_hb_watchdog)
        await commandbus.register(Commands.STOP_HB_WATCHDOG, heartbeat_service.stop_hb_watchdog)
        await commandbus.register(Commands.START_HB_LOOP, heartbeat_service.start_hb_loop)
        await commandbus.register(Commands.STOP_HB_LOOP, heartbeat_service.stop_hb_loop)
        await commandbus.register(Commands.SEND_ONE_HEARTBEAT, heartbeat_service.send_heartbeat)

        await commandbus.register(Commands.START_LISTENER, handle_responses.start_listener)
        await commandbus.register(Commands.STOP_LISTENER, handle_responses.stop_listener)
        await commandbus.register(Commands.HANDLE_EVENT, handle_events.handle_events)

        await websocket_handler.reset()

        await self.stop.wait()