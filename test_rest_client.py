from betterbot.rest_client.wrapper import HttpWrapper
from betterbot.rest_client.error import Types
import logging
import asyncio
import json

class Test:
    def __init__(self):
        with open("config.json") as f:
            config = json.load(f)

        logging.basicConfig(level=logging.DEBUG, filename="log.txt", filemode="w")
        self.logger = logging.getLogger("TEST_SCRIPT")
        self.wrapper = HttpWrapper(token="")

    async def debug_wrapper(self):
        channel_ids = []
        here = 0
        json = None
        method = "get"
        for l in range(10):
            for i in channel_ids:
                here += 1
                if here <= 17:
                    endpoint = f"https://discord.com/api/v9/channels/{i}/messages?limit=20"

                response = await self.wrapper.request(method=method, endpoint=endpoint, identifier=f"{method}:{i}", json=json)
                if response in [Types.CONNECTION_FAILED, Types.FAILED, Types.SUCCESS]:
                    self.logger.critical(response)

                if here == 20:
                    self.logger.critical("Changing endpoint to a valid one and sending messages.")
                    method = "post"
                    endpoint = f"https://discord.com/api/v9/channels/{i}/messages"
                    json = {"content": "I am nice jk."}
                    
                elif here == 17:
                    self.logger.critical("Changing endpoint to invalid.")
                    endpoint = "https://discordsucks69696969696.com"

                elif here == 12:
                    self.logger.critical("Clearing listeners")
                    self.wrapper.listeners.clear() # Removing reference should recover.

                elif here == 35:
                    break
            

asyncio.run(Test().debug_wrapper())