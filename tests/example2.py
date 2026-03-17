from betterbot import Setup, Intents, Events
from example2depend import Ban
import asyncio
import json
from betterbot import CommandTypes

class Bot:
    def __init__(self):
        with open("config.json") as f:
            self.config = json.load(f)
        
        token = self.config["token"]
        mod_roles = self.config["mod_roles"]
        ban_role = self.config["ban_role"]

        self.guild = self.config["guild"]    

        self.bot = Setup(token=token, intents=Intents.all)
        self.bot.debug_logs = False
        self.event = self.bot.event
        self.rest_client = self.bot.rest_client
        self.ban = Ban(mod_roles, self.rest_client, self.guild, ban_role)
        self.tasks = set() # Needed to avoid GC

    async def start(self):
        await self.event.register(Events.BOT_READY, self.on_ready)
        await self.bot.start()

    async def on_ready(self, username, application_id):
        options = [{
            "name": "user", 
            "type": CommandTypes.USER, 
            "description": "User to ban",
            "required": True,
            },
            {
                "name": "unit",
                "description": "Unit of time",
                "type": CommandTypes.STRING,
                "required": True,
                "choices": [
                    {"name": "Minutes", "value": "minutes"},
                    {"name": "Hours", "value": "hours"},
                    {"name": "Days", "value": "days"},
                ]
            },
            {
                "name": "duration",
                "description": "Amount",
                "type": CommandTypes.INTEGER,
                "required": True,
            },
            ]
        
        await self.rest_client.create_guild_command(self.ban.ban, application_id=application_id, guild_id=self.guild, name="ban", description="Ban a user", options=options)
    
        options = [{
            "name": "user",  
            "description": "User to unban",
            "type": CommandTypes.USER,
            "required": True
        }]

        await self.rest_client.create_guild_command(self.ban.unban, application_id=application_id, guild_id=self.guild, name="unban", description="Unban someone", options=options)

        task = asyncio.create_task(self.ban.polling_unban())
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

        print(f"Logged in as {username}")

asyncio.run(Bot().start())