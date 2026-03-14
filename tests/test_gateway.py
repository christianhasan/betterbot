import json
import asyncio
import logging
from .. import Setup
from ..gateway_client.command_related.commands import Commands

class Test:
    def __init__(self):
        self.setup = Setup(token="I like stuff", intents="I do too")
        self.logger = logging.getLogger(__name__)
        self.setup.debug_logs = True
        self.setup.test_mode = True
        self.commandbus_flag = False
        self.eventbus_flag = False
        self.times = 0
        self.success_count = 0

    async def mock_command_receiver(self, **kwargs):
        if not kwargs:
            self.logger.info(f"mock_command_receiver received nothing. 41298491")
        else:
            self.logger.info(f"mock_command_receiver received {kwargs}. 41298491")

    async def mock_eventbus_receiver(self, times):
        self.times += 1
        print(f"You should see me {times}")
        return 69

    async def debug_commandbus(self):
        try:
            await self.commandbus.emit("text")
        except RuntimeError:
            self.logger.info("Commandbus successfully threw error when there is nothing registered 34872783")
            self.success_count += 1

        try:
            await self.commandbus.register("test", lambda: self.mock_eventbus_receiver(times=2))
            await self.commandbus.register("test", lambda: self.mock_eventbus_receiver(times=2))
        except RuntimeError:
            self.logger.info("Commandbus correctly raised exception. 93242873")
            self.success_count += 1

        finally:
            nothing = await self.commandbus.emit("test", fire_and_forget=True)
            something = await self.commandbus.emit("test", fire_and_forget=False)
            await asyncio.sleep(1)

            assert something == 69, "Return values not expected"

        self.logger.warning("COMMANDBUS DEBUGGING FINISHED")

    async def debug_heartbeat_service(self):
        self.session.sequence = 5
        self.session.heartbeat_interval = 2

        response = await self.heartbeat_service._start_heartbeat_watchdog()
    
        assert response == "WATCHDOG_TRIGGERED", "Watchdog not triggered."
        self.success_count += 1

        response = await self.heartbeat_service.send_heartbeat()
        assert response == "SENT", "Heartbeat not working as expected"
        self.success_count += 1
        
        self.logger.warning("HEARTBEAT SERVICE DEBUGGING FINISHED 12483251")

    async def debug_eventbus(self):
        asyncio.create_task(self.eventbus.wait_for_event("test696969"))

        await self.eventbus.register("test696969", lambda: self.mock_eventbus_receiver(times=3), lambda: self.mock_eventbus_receiver(times=3))
        await self.eventbus.register("test696969", lambda: self.mock_eventbus_receiver(times=3))

        await self.eventbus.emit("test696969")

        self.logger.warning("EVENTBUS DEBUGGING FINISHED 01958235")

    async def debug_reset_websocket_handler(self): # Error prone therefore it has it's own function
        self.websocket_handler.reset_running = True

        message = await self.websocket_handler.reset()

        assert message == "BUSY", "The websocket reset function continued running even tho flag is set. 103248124"

        self.websocket_handler.reset_running = False
        self.websocket_handler.gateway_url = "wss://ws.ifelse.io"

        await self.websocket_handler.reset()

        await self.websocket_handler.ws.close()

        self.websocket_handler.gateway_url = "I am invalid"

        task = asyncio.create_task(self.websocket_handler.reset())

        await asyncio.sleep(10)
        self.logger.info("You should have seen some reconnect attempts failing. 29913189")
        task.cancel()

        self.websocket_handler.gateway_url = "wss://ws.ifelse.io"
        task = asyncio.create_task(self.websocket_handler.send_websocket_message(self)) # Will throw error and try to reset.
        await asyncio.sleep(10)
        task.cancel()
        self.logger.info("You should have seen some reconnect attempts working. 1284184")

        self.logger.warning("WEBSOCKET RESET HANDLER DEBUGGING FINISHED 1942925")

    async def debug_websocket_handler(self):
        self.websocket_handler.ws = self

        await self.websocket_handler.send_websocket_message("I like beautiful women.")
        await self.websocket_handler.receive_message()

        self.logger.warning("WEBSOCKET HANDLER DEBUGGING FINISHED 42356463")

    async def send(self, data):
        print(f"I like cool women. What about you? {data} 10994771")

    async def recv(self):
        return json.dumps("I hate cool women.")
    
    async def debug(self, debug_all=True):
        result = await self.setup.start()

        (self.commandbus, self.session, self.identify, self.heartbeat_service,
        self.handle_responses, self.websocket_handler, self.eventbus) = result

        await self.commandbus.register(Commands.STOP_HB_WATCHDOG, self.mock_command_receiver)
        await self.commandbus.register(Commands.STOP_HB_LOOP, self.mock_command_receiver)
        await self.commandbus.register(Commands.STOP_LISTENER, self.mock_command_receiver)
        await self.commandbus.register(Commands.SEND_WEBSOCKET_MESSAGE, self.mock_command_receiver)
        await self.commandbus.register(Commands.START_LISTENER, self.mock_command_receiver)
        await self.commandbus.register(Commands.CLIENT_RESET_NEEDED, self.websocket_handler.reset)

        if debug_all is True:
            await self.debug_websocket_handler()
            await self.debug_reset_websocket_handler()
            await self.debug_eventbus()
            await self.debug_commandbus()
            await self.debug_heartbeat_service()
            assert self.times == 5, "Times receiver ran not matching expected"
            assert self.success_count == 4
        else:
            return self.debug_websocket_handler, self.debug_reset_websocket_handler, self.debug_eventbus, self.debug_commandbus, self.debug_heartbeat_service

debug = asyncio.run(Test().debug(debug_all=True))
#asyncio.run(debug[2]())
