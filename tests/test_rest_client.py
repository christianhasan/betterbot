from ..rest_client.wrapper import HttpWrapper
import logging
import asyncio
import sys

class Test:
    def __init__(self):
        self.tasks = set()
        self.spam_mode = False
        
        token = ""

        sys.stdout.reconfigure(encoding="utf-8")

        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler("log.txt", mode="w", encoding="utf-8"),
                logging.StreamHandler(sys.stdout)
            ],
        )

        self.wrapper = HttpWrapper(token=token)

    async def debug_wrapper(self):
        channel_ids = [1482287900585496706, 1482287927206740008]
        json = {"content": "I am nice jk."}
        method = "post"
        if self.spam_mode is True:
            for l in range(100):
                for i in channel_ids:
                    endpoint = f"https://discord.com/api/v9/channels/{i}/messages"
                    task = asyncio.create_task(self.wrapper.request(method=method, endpoint=endpoint, identifier=f"{method}:{i}", json=json))
                    self.tasks.add(task)
                    task.add_done_callback(self.tasks.discard)
        else:
            for l in range(100):
                for i in channel_ids:
                    endpoint = f"https://discord.com/api/v9/channels/{i}/messages"
                    result = await self.wrapper.request(method=method, endpoint=endpoint, identifier=f"{method}:{i}", json=json)
                    print(result)

        await asyncio.Future()
asyncio.run(Test().debug_wrapper())