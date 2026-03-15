# Betterbot

A modern, event-driven bot framework for Python, designed for simplicity and flexibility.

## Install
Install via pip:

```bash
pip install betterbot
```

## How to Use
Import the `Setup` module and initialize your bot:

```python
from betterbot import Setup
```

### Example Bot Script

```python
import asyncio
import json
from betterbot import Setup, Events, InteractionTypes

# Load bot token from configuration
with open("config.json") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]

class Bot:
    def __init__(self):
        self.bot = Setup(TOKEN, intents=53608447)
        self.bot.debug = True  # Enable detailed debug logs
        self.rest = self.bot.rest_client
        self.bot_username = None
        self.event = self.bot.event

    async def main(self):
        # Register event handlers
        await self.event.register(Events.BOT_READY, self.on_ready) # You can register multiple handlers per event.
        await self.event.register(Events.MESSAGE_CREATE, self.on_message)
        await self.bot.start()

    # -----------------------
    # Event Handlers
    # -----------------------
    async def on_ready(self, username, es):
        self.bot_username = username
        print(f"Logged in as {username}")

        # Create a guild slash command
        await es.create_guild_command(
            self.test_command,
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
    # Slash Command Handler
    # -----------------------
    async def test_command(self, es): # Es stands for eventsend and is the prefered way to respond to events
        # Immediately respond to the interaction
        await es.respond_message(content="Hello, it is starting!")
        await self.test_rest_methods()

    async def test_rest_methods(self):
        # -----------------------
        # Channel Methods
        # -----------------------
        await self.rest.send_message(CHANNEL_ID, "Hello from Betterbot REST test!")

        messages = await self.rest.get_messages(CHANNEL_ID)
        if messages:
            msg_id = messages[0]["id"]
            await self.rest.typing(CHANNEL_ID)
            await self.rest.add_reaction(CHANNEL_ID, msg_id, "👍")
            await self.rest.remove_reaction(CHANNEL_ID, msg_id, "👍")
            await self.rest.pin_message(CHANNEL_ID, msg_id)
            await self.rest.unpin_message(CHANNEL_ID, msg_id)

        # -----------------------
        # Guild Methods
        # -----------------------
        guild_info = await self.rest.get_guild_info(GUILD_ID)
        members = await self.rest.get_guild_members(GUILD_ID, limit=5)
        roles = await self.rest.get_guild_roles(GUILD_ID)

        print("REST test complete!")

# -----------------------
# Run Bot
# -----------------------
asyncio.run(Bot().main())
```
