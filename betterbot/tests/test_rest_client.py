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
        json = {"content": "I am nice jk."}
        method = "post"
        for l in range(5):
            for i in channel_ids:
                endpoint = f"https://discord.com/api/v9/channels/{i}/messages"
                response = await self.wrapper.request(method=method, endpoint=endpoint, identifier=f"{method}:{i}", json=json)
                if response in [Types.CONNECTION_FAILED, Types.FAILED, Types.SUCCESS]:
                    self.logger.critical(response)
                    
                elif here == 35:
                    break
            

asyncio.run(Test().debug_wrapper())