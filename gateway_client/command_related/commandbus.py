import asyncio
import logging

class Commandbus:
    def __init__(self):
        self.registry = {}
        self.tasks = set()
        self.logger = logging.getLogger(__name__)

    async def register(self, command_type, handler):
        if command_type in self.registry:
            raise RuntimeError("Only one handler per command allowed!")

        self.registry.update({command_type: handler})

        self.logger.debug(f"Registered command {command_type} to {handler}")

    async def emit(self, command_type, fire_and_forget=False, **kwargs):
        if command_type not in self.registry:
            raise RuntimeError("Undefined command was called!")

        handler = self.registry[command_type]

        self.logger.debug(f"Emitting {command_type} to {handler}")

        if fire_and_forget is False:
            return await handler(**kwargs)
        else:
            task = asyncio.create_task(handler(**kwargs))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)