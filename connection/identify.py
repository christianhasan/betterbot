from ..command_related.commands import Commands
import logging

class Identify:
    def __init__(self, commandbus, session):
        self.logger = logging.getLogger(__name__)
        self.emit = commandbus.emit
        self.token = session.token

    async def identify(self):
        payload = {
            "op": 2,
            "d": {
            "token": self.token,
            "properties": {
                "os": "Windows",
                "browser": "Firefox",
                "device": "",
                "system_locale": "en-US",
                "has_client_mods": "false",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
                "browser_version": "145.0.0.0",
                "os_version": "10",
                "referrer": "https://www.google.com/",
                "referring_domain": "www.google.com",
                "search_engine": "google",
                "referrer_current": "",
                "referring_domain_current": "",
                "release_channel": "stable",
                },
            }
        }

        self.logger.debug("Identifying...")
        await self.emit(Commands.SEND_WEBSOCKET_MESSAGE, fire_and_forget=False, data=payload)