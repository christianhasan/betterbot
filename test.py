import json
import asyncio
import logging
from betterbot import Setup
from betterbot.command_related.commands import Commands

class FaultInjection:
    def __init__(self):
        self.logger = logging.getLogger()
        self.setup = Setup(token="I like stuff")
        self.setup.debug = True
        self.commandbus_flag = False
        self.eventbus_flag = False

    async def mock_command_receiver(self, **kwargs):
        if not kwargs:
            self.logger.info(f"mock_command_receiver received nothing. 41298491")

        else:
            self.logger.info(f"mock_command_receiver received {kwargs}. 1409891")

    async def debug_commandbus(self):
        if self.commandbus_flag is True:
            self.logger.info("Commandbus emitted. This should print twice. 32765732")
            return 69
        self.commandbus_flag = True
        try:
            await self.commandbus.emit("text")
        except RuntimeError:
            self.logger.info("Commandbus successfully threw error when there is nothing registered 34872783")

        try:
            await self.commandbus.register("test", self.debug_commandbus)
            await self.commandbus.register("test", self.debug_commandbus)
        except RuntimeError:
            self.logger.info("Commandbus correctly raised exception. 93242873")

        finally:
            nothing = await self.commandbus.emit("test", fire_and_forget=True)
            something = await self.commandbus.emit("test", fire_and_forget=False)
            await asyncio.sleep(1)
            if something == 69 and nothing is None:
                self.logger.info("Fire and forget and await working correctly. 149273298")
            else:
                self.logger.critical("ERROR ERROR ERROR. Commandbus is not working correctly. 12984197")

        self.logger.warning("COMMANDBUS DEBUGGING FINISHED")

        self.commandbus_flag = False

    async def debug_heartbeat_service(self):
        self.session.sequence = 5
        self.session.heartbeat_interval = 2

        for i in range(4):
            await self.heartbeat_service.start_hb_watchdog()
    
        await asyncio.sleep(5)
        self.logger.info("Did you hear a dog barking? If yes then good. If not then ERROR ERROR ERROR 128940981")

        await self.heartbeat_service.send_heartbeat()

        for i in range(4):
            await self.heartbeat_service.start_hb_loop()

        await asyncio.sleep(6)
        await self.heartbeat_service.stop_hb_loop()
        self.logger.info("Did it send multiple heartbeats and get cancelled? If yes then good if not then ERROR ERROR ERROR 31498891")
        
        self.logger.warning("HEARTBEAT SERVICE DEBUGGING FINISHED 12483251")

    async def debug_eventbus(self):
        if self.eventbus_flag is True:
            self.logger.info("I should be here three times 412489037")
            return
        self.eventbus_flag = True    

        asyncio.create_task(self.eventbus.wait_for_event("test696969"))

        await self.eventbus.register("test696969", self.debug_eventbus, self.debug_eventbus)
        await self.eventbus.register("test696969", self.debug_eventbus)

        await self.eventbus.emit("test696969")

        await asyncio.sleep(3)

        self.eventbus_flag = False

        self.logger.warning("EVENTBUS DEBUGGING FINISHED 01958235")

    async def debug_reset_websocket_handler(self): # Error prone therefore it has it's own function
        self.websocket_handler.reset_running = True

        message = await self.websocket_handler.reset()

        if message != 22:
            self.logger.critical("The program continued running even tho flag is set. 103248124")

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
        else:
            return self.debug_websocket_handler, self.debug_reset_websocket_handler, self.debug_eventbus, self.debug_commandbus, self.debug_heartbeat_service

debug = asyncio.run(FaultInjection().debug(debug_all=True))
#asyncio.run(debug[2]())
