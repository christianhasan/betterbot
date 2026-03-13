from ..command_related.commands import Commands
import logging

class Identify:
    def __init__(self, commandbus, session):
        self.logger = logging.getLogger(__name__)
        self.emit = commandbus.emit
        self.token = session.token
        self.intents = session.intents

    async def identify(self):
        payload = {
            "op": 2,
            "d": {
            "token": self.token,
            "intents": self.intents,
            "properties": {
                "os": "Windows",
                "browser": "Betterbot",
                "device": "Betterbot",
                },
            }
        }

        self.logger.debug("Identifying...")
        await self.emit(Commands.SEND_WEBSOCKET_MESSAGE, fire_and_forget=False, data=payload)