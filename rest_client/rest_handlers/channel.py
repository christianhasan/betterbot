from .endpoints import Endpoints

class Channel:
    def __init__(self, wrapper):
        self.send = wrapper.request

    async def get_channel_info(self, channel_id):
        endpoint = Endpoints.CHANNEL(d={"channel_id": channel_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_channel_info:{channel_id}")

    async def send_message(self, channel_id, content=None, embed=None, components=None):
        if not content and not embed and not components:
            raise ValueError("At least one of content, embed, or components must be provided")
        payload = {}
        if content: payload["content"] = content
        if embed: payload["embeds"] = embed
        if components: payload["components"] = components
        endpoint = Endpoints.CHANNEL_MESSAGES(d={"channel_id": channel_id})
        return await self.send(method="post", endpoint=endpoint, identifier=f"send_message:{channel_id}", json=payload)

    async def get_messages(self, channel_id, limit=100, before_id=None):
        endpoint = Endpoints.CHANNEL_MESSAGES(d={"channel_id": channel_id}) + (f"?limit={limit}" if before_id is None else f"?limit={limit}&before={before_id}")
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_messages:{channel_id}")

    async def get_message(self, channel_id, message_id):
        endpoint = Endpoints.CHANNEL_MESSAGE(d={"channel_id": channel_id, "message_id": message_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_message:{channel_id}")

    async def delete_message(self, channel_id, message_id):
        endpoint = Endpoints.CHANNEL_MESSAGE(d={"channel_id": channel_id, "message_id": message_id})
        return await self.send(method="delete", endpoint=endpoint, identifier=f"delete_message:{channel_id}")

    async def add_reaction(self, channel_id, message_id, emoji, user_id=None):
        if user_id: endpoint = Endpoints.CHANNEL_REACTION_USER(d={"channel_id": channel_id, "message_id": message_id, "emoji": emoji, "user_id": user_id})
        else: endpoint = Endpoints.CHANNEL_REACTIONS(d={"channel_id": channel_id, "message_id": message_id, "emoji": emoji})
        return await self.send(method="put", endpoint=endpoint, identifier=f"add_reaction:{channel_id}")

    async def remove_reaction(self, channel_id, message_id, emoji, user_id=None):
        if user_id: endpoint = Endpoints.CHANNEL_REACTION_USER(d={"channel_id": channel_id, "message_id": message_id, "emoji": emoji, "user_id": user_id})
        else: endpoint = Endpoints.CHANNEL_REACTIONS(d={"channel_id": channel_id, "message_id": message_id, "emoji": emoji})
        return await self.send(method="delete", endpoint=endpoint, identifier=f"remove_reaction:{channel_id}")

    async def bulk_delete_messages(self, channel_id, message_ids):
        payload = {"messages": message_ids}
        endpoint = Endpoints.CHANNEL_BULK_DELETE_MESSAGES(d={"channel_id": channel_id})
        return await self.send(method="post", endpoint=endpoint, identifier=f"bulk_delete:{channel_id}", json=payload)

    async def get_pins(self, channel_id):
        endpoint = Endpoints.CHANNEL_PINS(d={"channel_id": channel_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_pins:{channel_id}")

    async def pin_message(self, channel_id, message_id):
        endpoint = Endpoints.CHANNEL_PIN(d={"channel_id": channel_id, "message_id": message_id})
        return await self.send(method="put", endpoint=endpoint, identifier=f"pin_message:{channel_id}")

    async def unpin_message(self, channel_id, message_id):
        endpoint = Endpoints.CHANNEL_PIN(d={"channel_id": channel_id, "message_id": message_id})
        return await self.send(method="delete", endpoint=endpoint, identifier=f"unpin_message:{channel_id}")

    async def typing(self, channel_id):
        endpoint = Endpoints.CHANNEL_TYPING(d={"channel_id": channel_id})
        return await self.send(method="post", endpoint=endpoint, identifier=f"typing:{channel_id}")
    
    async def delete_channel(self, channel_id):
        endpoint = Endpoints.CHANNEL(d={"channel_id": channel_id})
        return await self.send(method="delete", endpoint=endpoint, identifier=f"delete_channel:{channel_id}")

    async def create_channel(self, guild_id, name, channel_type, topic=None, parent_id=None, voice_user_limit=None, nsfw=False):
        endpoint = Endpoints.CHANNEL_CREATE(d={"guild_id": guild_id})
        payload = {
            "name": name,
            "type": channel_type,
        }
        if topic: payload["topic"] = topic
        if parent_id: payload["parent_id"] = parent_id
        if voice_user_limit: payload["user_limit"] = voice_user_limit
        if nsfw: payload["nsfw"] = nsfw

        return await self.send(method="post", endpoint=endpoint, identifier=f"create_channel:{guild_id}", json=payload)
    
    async def set_channel_permissions(self, channel_id, overwrite_id, is_role=False, allow=None, deny=None):
        endpoint = Endpoints.CHANNEL_PERMISSIONS(d={"channel_id": channel_id, "overwrite_id": overwrite_id})
        if is_role == True: overwrite_type = 0
        else: overwrite_type = 1
        payload = {
            "type": overwrite_type,
            "deny": deny,
            "allow": allow,
        }
        return await self.send(method="put", endpoint=endpoint, identifier=f"put:{channel_id}", json=payload)