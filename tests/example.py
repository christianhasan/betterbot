import asyncio
import json
from betterbot import Setup, Events, InteractionTypes, Types

# Load bot token
with open("config.json") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]

class Bot:
    def __init__(self):
        self.bot = Setup(TOKEN, intents=53608447)
        self.bot.debug = True # Debug mode for enabling comprehensive logs. You must have a instance of Setup first. 
        self.rest = self.bot.rest_client
        self.bot_username = None
        self.event = self.bot.event

    async def main(self):
        await self.event.register(Events.BOT_READY, self.on_ready) # You can add multiple events
        await self.event.register(Events.MESSAGE_CREATE, self.on_message)
        await self.bot.start()

    # -----------------------
    # Events
    # -----------------------
    async def on_ready(self, username, application_id):
        self.bot_username = username
        print(f"Logged in as {username}")

        # Create a guild slash command
        await self.rest.create_guild_command(
            self.test_command,
            application_id=application_id,
            guild_id=GUILD_ID,
            name="testrest",
            description="Test all REST endpoints with defer"
        )

    async def on_message(self, username, content, channel_id):
        if username == self.bot_username:
            return
        print(f"{username}: {content}")
        if content.lower() == "test rest":
            await self.test_rest_methods()

    # -----------------------
    # Slash command handler
    # -----------------------
    async def test_command(self, interaction_id, token):
        # Defer the interaction immediately
        id = await self.rest.send_interaction_callback(
            interaction_id,
            token,
            cmd_type=InteractionTypes.RESPOND_WITH_MESSAGE,
            content="Hello it is starting!"
        )
        await self.test_rest_methods()


    async def test_rest_methods(self):
        # Some channel methods
        # -------------------

        await self.rest.send_message(CHANNEL_ID, "Hello from betterbot REST test!")

        messages = await self.rest.get_messages(CHANNEL_ID)
        for i in range(1):
            id = messages[0]["id"]

        await self.rest.typing(CHANNEL_ID)
        await self.rest.add_reaction(CHANNEL_ID, id, "👍")
        await self.rest.remove_reaction(CHANNEL_ID, id, "👍")
        await self.rest.pin_message(CHANNEL_ID, id)
        await self.rest.unpin_message(CHANNEL_ID, id)
        messages = await self.rest.get_messages(CHANNEL_ID, limit=5)

        # -------------------
        # Guild methods
        # -------------------

        guild_info = await self.rest.get_guild_info(GUILD_ID)
        members = await self.rest.get_guild_members(GUILD_ID, limit=5)
        roles = await self.rest.get_guild_roles(GUILD_ID)

        print("REST test complete!")

# -----------------------
# Run bot
# -----------------------
asyncio.run(Bot().main())