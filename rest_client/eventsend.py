from typing import Optional, Any, Callable
from .rest_handlers.interaction import InteractionTypes

class es:
    rest_client = None

    def __init__(self, **kwargs):
        self.application_id = None
        self.channel = None
        self.interaction_id = None
        self.interaction_token = None

        for key, value in kwargs.items():
            setattr(self, key, value)


    async def create_global_command(self, *handlers: Callable, name: str, description: str, options: Optional[list] = None, cmd_type: int = 1) -> Any:
        """Create a new global application command."""
        if self.application_id is None:
            raise RuntimeError("You cannot register a command via Event Send (es) when there isn't an event with application ID. You should use this command in bot ready event.")
        
        return await es.rest_client.create_global_command(*handlers, application_id=self.application_id, name=name, description=description, options=options, cmd_type=cmd_type)

    async def create_guild_command(self, *handlers: Callable, guild_id: str, name: str, description: str, options: Optional[list] = None, cmd_type: int = 1) -> Any:
        """Create a new guild-specific application command."""

        if self.application_id is None:
            raise RuntimeError("You cannot register a command via Event Send (es) when there isn't an event with application ID. You should use this command in bot ready event.")
        
        return await es.rest_client.create_guild_command(*handlers, application_id=self.application_id, guild_id=guild_id, name=name, description=description, options=options, cmd_type=cmd_type)

    async def send(self, content: Optional[str] = None, embed: Optional[list] = None, components: Optional[list] = None) -> Any:
        """
        Send a message to a channel.
        
        Args:
            content: Text content of the message.
            embed: Optional embed dictionary.
            components: Buttons and such.
        """
        if self.channel is None:
            raise RuntimeError("You cannot send a message via Event Send (es) when there isn't an event with channel information.")
        
        return await es.rest_client.send_message(self.channel, content, embed, components)
    
    async def respond_message(self, content: Optional[str] = None, embed: Optional[list] = None, components: Optional[list] = None, ephemeral: bool = False) -> Any:
        """Send an interaction message response."""

        if self.interaction_id is None or self.interaction_token is None:
            raise RuntimeError("You cannot send a message via Event Send (es) when there isn't a command invoker.")

        return await es.rest_client.send_interaction_callback(self.interaction_id, self.interaction_token, InteractionTypes.RESPOND_WITH_MESSAGE, content, embed, components, ephemeral)

    async def send_interaction_callback(self, cmd_type: int, content: Optional[str] = None, embed: Optional[list] = None, components: Optional[list] = None, ephemeral: bool = False) -> Any:
        """Send an interaction response."""

        if self.interaction_id is None or self.interaction_token is None:
            raise RuntimeError("You cannot send an interaction callback via Event Send (es) when there isn't a command invoker.")

        return await es.rest_client.send_interaction_callback(self.interaction_id, self.interaction_token, cmd_type, content, embed, components, ephemeral)

    async def send_interaction_followup(self, content: Optional[str] = None, embed: Optional[list] = None, components: Optional[list] = None, ephemeral: bool = False) -> Any:
        """Send an interaction follow-up."""

        if self.application_id is None or self.interaction_token is None:
            raise RuntimeError("You cannot send a follow-up via Event Send (es) when there isn't a command invoker.")

        return await es.rest_client.send_interaction_followup(self.application_id, self.interaction_token, content, embed, components, ephemeral)
    
    async def get_original_interaction_message(self):
        """Retrieve the original interaction message."""
        
        if self.application_id is None or self.interaction_token is None:
            raise RuntimeError("You cannot send a get interaction message via Event Send (es) when there isn't a command invoker.")

        return await es.rest_client.get_original_interaction_message(self.application_id, self.interaction_token)
    
    async def update_interaction_message(self, content: Optional[str] = None, embed: Optional[list] = None, components: Optional[list] = None, message_id: Optional[str] = None) -> Any:
        """Update an interaction message, optionally specifying message ID."""

        if self.application_id is None or self.interaction_token is None:
            raise RuntimeError("You cannot update a interactiong message via Event Send (es) when there isn't a command invoker.")


        return await es.rest_client.update_interaction_message(self.application_id, self.interaction_token, content, embed, components, message_id)