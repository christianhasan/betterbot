import asyncio
from .events import Events
from ...rest_client.eventsend import es
import logging
import inspect

class EventBus:
    def __init__(self, rest_client):
        self.logger = logging.getLogger(__name__)
        self.rest_client = rest_client
        self.registry = {}
        self.waiters = {}
        self.tasks = set() # Required to avoid garbage collection.

    async def register(self, event_type, *handlers):
        self.logger.debug(f"Registering {event_type} for {handlers}")
        if event_type not in self.registry:
            self.registry[event_type] = []
        
        self.registry[event_type].extend(handlers)

    async def unregister(self, event_type, handler=None):
        if event_type in self.registry:
            if handler is None:
                self.logger.debug(f"Unregistering all handlers in {event_type}")
                del self.registry[event_type]
            else:
                self.logger.debug(f"Unregistering {handler} for {event_type}")
                if handler in self.registry[event_type]:
                    self.registry[event_type].remove(handler)

    async def emit(self, event_type, **kwargs):
        self.logger.debug(f"Emitting {event_type} with {kwargs}")
        handlers = self.registry.get(event_type, [])
        self.logger.debug(f"Handlers registered for {event_type} is {handlers} and they are now gonna be executed.")

        for handler in self.registry.get(Events.EVERYTHING, []):
            self.logger.debug(f"Everything handler exists.")
            task = asyncio.create_task(handler(event_type, **kwargs))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)
            self.logger.debug(f"Notified everything handler for {event_type}")

        for handler in handlers:
            allowed_params = inspect.signature(handler).parameters.keys()
            filtered_params = {param_name: value for param_name, value in kwargs.items() if param_name in allowed_params}
            
            if "es" in allowed_params:
                filtered_params["es"] = es(self.rest_client, **kwargs)

            self.logger.debug(f"Notifying {handler} for {event_type}")

            task = asyncio.create_task(handler(**filtered_params))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

        for waiter in self.waiters.get(event_type, []):
            self.logger.debug(f"Notified waiters for {event_type}")
            waiter.set()

    async def wait_for_event(self, event_type):
        if event_type not in self.waiters:
            self.waiters[event_type] = []

        event = asyncio.Event()
        self.waiters[event_type].append(event)

        await event.wait()

        self.waiters[event_type].remove(event)