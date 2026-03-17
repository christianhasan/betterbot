from .gateway_client.handlers.websocket_handler import WebsocketHandler
from .gateway_client.command_related.commandbus import Commandbus
from .gateway_client import error
from .gateway_client.command_related.commands import Commands
from .gateway_client.connection.identify import Identify
from .gateway_client.connection.heartbeatservice import HeartbeatService
from .gateway_client.connection.session import Session
from .gateway_client.event_related.eventbus import EventBus
from .gateway_client.handlers.handle_responses import HandleResponses
from .gateway_client.event_related.handle_event_responses import HandleEventResponses
from .rest_client.restclient import RESTClient

import sys
import asyncio
import logging

class Setup:
    def __init__(self, token: str, intents: int):
        if token is None:
            raise error.InvalidTokenError("You must provide your discord token.")
        
        if intents is None:
            raise error.InvalidIntentsError("You must provide Intents.")

        self.debug_logs = False
        self.test_mode = False

        self.token = token
        self.intents = intents

        self.rest_client = RESTClient(token, self.event)
        self.event = EventBus(self.rest_client)

        self.stop = asyncio.Event()

    def _start_logging(self):
        sys.stdout.reconfigure(encoding="utf-8")
        logging.basicConfig(
            level=logging.DEBUG if self.debug_logs else logging.WARNING,
            handlers=[
                logging.FileHandler("log.txt", mode="w", encoding="utf-8"),
                logging.StreamHandler(sys.stdout)
            ],
        )

    async def start(self):
        self._start_logging()

        commandbus = Commandbus()
        session = Session()

        session.token = self.token
        session.intents = self.intents

        websocket_handler = WebsocketHandler(commandbus)
        handle_events = HandleEventResponses(self.event, session)
        identify = Identify(commandbus, session)
        heartbeat_service = HeartbeatService(commandbus, session)
        handle_responses = HandleResponses(commandbus, session)


        if self.test_mode is True:
            return commandbus, session, identify, heartbeat_service, handle_responses, websocket_handler, self.event

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