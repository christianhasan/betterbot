from typing import Any, List, Optional
from .interaction.interaction import Interaction
from .guild.guild import Guild
from .channel.channel import Channel
from wrapper import HttpWrapper

class RESTClient:
    def __init__(self, token):
        wrapper = HttpWrapper(token)

        self.channel = Channel(wrapper)
        self.guild = Guild(wrapper)
        self.interaction = Interaction(wrapper)

    # -------------------------
    # CHANNEL METHODS
    # -------------------------

    async def send_message(self, channel_id: str, content: Optional[str] = None, embed: Optional[dict] = None, file: Optional[Any] = None) -> Any:
        """
        Send a message to a channel.
        
        Args:
            channel_id: ID of the channel.
            content: Text content of the message.
            embed: Optional embed dictionary.
            file: Optional file to send.
        """
        return await self.channel.send_message(channel_id, content, embed, file)

    async def get_messages(self, channel_id: str, limit: int = 100, before_id: Optional[str] = None) -> Any:
        """Retrieve messages from a channel, optionally before a specific message ID."""
        return await self.channel.get_messages(channel_id, limit, before_id)

    async def delete_message(self, channel_id: str, message_id: str) -> Any:
        """Delete a specific message in a channel."""
        return await self.channel.delete_message(channel_id, message_id)

    async def add_reaction(self, channel_id: str, message_id: str, emoji: str) -> Any:
        """Add a reaction to a message."""
        return await self.channel.add_reaction(channel_id, message_id, emoji)

    async def remove_reaction(self, channel_id: str, message_id: str, emoji: str, user_id: Optional[str] = None) -> Any:
        """Remove a reaction from a message, optionally for a specific user."""
        return await self.channel.remove_reaction(channel_id, message_id, emoji, user_id)

    async def bulk_delete_messages(self, channel_id: str, message_ids: List[str]) -> Any:
        """Bulk delete multiple messages from a channel."""
        return await self.channel.bulk_delete_messages(channel_id, message_ids)

    async def get_pins(self, channel_id: str) -> Any:
        """Get all pinned messages in a channel."""
        return await self.channel.get_pins(channel_id)

    async def pin_message(self, channel_id: str, message_id: str) -> Any:
        """Pin a message in a channel."""
        return await self.channel.pin_message(channel_id, message_id)

    async def unpin_message(self, channel_id: str, message_id: str) -> Any:
        """Unpin a message in a channel."""
        return await self.channel.unpin_message(channel_id, message_id)

    async def trigger_typing(self, channel_id: str) -> Any:
        """Trigger typing indicator in a channel."""
        return await self.channel.typing(channel_id)

    # -------------------------
    # GUILD METHODS
    # -------------------------

    async def get_guild_info(self, guild_id: str) -> Any:
        """Retrieve information about a guild."""
        return await self.guild.get_guild_info(guild_id)

    async def get_guild_members(self, guild_id: str, limit: int = 100, after: Optional[str] = None) -> Any:
        """Retrieve a list of guild members."""
        return await self.guild.get_guild_members(guild_id, limit, after)

    async def get_guild_member(self, guild_id: str, user_id: str) -> Any:
        """Retrieve information about a specific guild member."""
        return await self.guild.get_guild_member(guild_id, user_id)

    async def get_guild_roles(self, guild_id: str) -> Any:
        """Get all roles in a guild."""
        return await self.guild.get_guild_roles(guild_id)

    async def get_guild_role(self, guild_id: str, role_id: str) -> Any:
        """Retrieve information about a specific role."""
        return await self.guild.get_guild_role(guild_id, role_id)

    async def add_member_role(self, guild_id: str, user_id: str, role_id: str) -> Any:
        """Add a role to a guild member."""
        return await self.guild.add_member_role(guild_id, user_id, role_id)

    async def remove_member_role(self, guild_id: str, user_id: str, role_id: str) -> Any:
        """Remove a role from a guild member."""
        return await self.guild.remove_member_role(guild_id, user_id, role_id)

    async def get_guild_bans(self, guild_id: str) -> Any:
        """Get a list of banned users in a guild."""
        return await self.guild.get_guild_bans(guild_id)

    async def get_guild_ban(self, guild_id: str, user_id: str) -> Any:
        """Get information about a specific guild ban."""
        return await self.guild.get_guild_ban(guild_id, user_id)

    async def prune_guild_members(self, guild_id: str, days: Optional[int] = None, compute_prune_count: bool = False) -> Any:
        """Prune inactive members from a guild."""
        return await self.guild.prune_guild_members(guild_id, days, compute_prune_count)

    async def get_guild_channels(self, guild_id: str) -> Any:
        """Get all channels in a guild."""
        return await self.guild.get_guild_channels(guild_id)

    # -------------------------
    # INTERACTION METHODS
    # -------------------------

    async def send_interaction_callback(self, interaction_id: str, interaction_token: str, content: Optional[str] = None, embed: Optional[dict] = None, components: Optional[list] = None) -> Any:
        """Send an interaction callback response."""
        return await self.interaction.send_interaction_callback(interaction_id, interaction_token, content, embed, components)

    async def send_interaction_followup(self, application_id: str, interaction_token: str, content: Optional[str] = None, embed: Optional[dict] = None, components: Optional[list] = None) -> Any:
        """Send a follow-up message for an interaction."""
        return await self.interaction.send_interaction_followup(application_id, interaction_token, content, embed, components)

    async def get_original_interaction_message(self, application_id: str, interaction_token: str) -> Any:
        """Retrieve the original interaction message."""
        return await self.interaction.get_original_interaction_message(application_id, interaction_token)

    async def update_interaction_message(self, application_id: str, interaction_token: str, content: Optional[str] = None, embed: Optional[dict] = None, components: Optional[list] = None, message_id: Optional[str] = None) -> Any:
        """Update an interaction message, optionally specifying message ID."""
        return await self.interaction.update_interaction_message(application_id, interaction_token, content, embed, components, message_id)