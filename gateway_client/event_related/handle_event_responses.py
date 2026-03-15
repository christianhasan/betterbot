from .events import Events
import logging

class HandleEventResponses:
    def __init__(self, eventbus, session):
        self.session = session
        self.emit = eventbus.emit
        self.logger = logging.getLogger(__name__)

        self.dispatch_map = {
            # Lifecycle
            Events.BOT_READY: lambda d: {
                "user_id": d.get("user", {}).get("id"),
                "username": d.get("user", {}).get("username"),
                "guilds": d.get("guilds"),
                "session_id": d.get("session_id"),
                "application_id": d.get("application", {}).get("id"),
                "payload": d,  # full raw payload
            },

            # Guild
            Events.GUILD_CREATE: lambda d: {
                "guild_id": d.get("id"),
                "name": d.get("name"),
                "payload": d
            },
            Events.GUILD_UPDATE: lambda d: {
                "guild_id": d.get("id"),
                "name": d.get("name"),
                "payload": d
            },
            Events.GUILD_DELETE: lambda d: {
                "guild_id": d.get("id"),
                "unavailable": d.get("unavailable"),
                "payload": d
            },

            # Member
            Events.GUILD_MEMBER_ADD: lambda d: {
                "guild_id": d.get("guild_id"),
                "user_id": d.get("user", {}).get("id"),
                "username": d.get("user", {}).get("username"),
                "payload": d
            },
            Events.GUILD_MEMBER_REMOVE: lambda d: {
                "guild_id": d.get("guild_id"),
                "user_id": d.get("user", {}).get("id"),
                "username": d.get("user", {}).get("username"),
                "payload": d
            },
            Events.GUILD_MEMBER_UPDATE: lambda d: {
                "guild_id": d.get("guild_id"),
                "user_id": d.get("user", {}).get("id"),
                "username": d.get("user", {}).get("username"),
                "payload": d
            },

            # Message
            Events.MESSAGE_CREATE: lambda d: {
                "message_id": d.get("id"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "user_id": d.get("author", {}).get("id"),
                "username": d.get("author", {}).get("username"),
                "content": d.get("content"),
                "embeds": d.get("embeds", []),
                "payload": d,
            },
            Events.MESSAGE_UPDATE: lambda d: {
                "message_id": d.get("id"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "content": d.get("content"),
                "payload": d,
            },
            Events.MESSAGE_DELETE: lambda d: {
                "message_id": d.get("id"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "payload": d,
            },
            Events.MESSAGE_DELETE_BULK: lambda d: {
                "message_ids": d.get("ids"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "payload": d,
            },

            # Reaction
            Events.MESSAGE_REACTION_ADD: lambda d: {
                "user_id": d.get("user_id"),
                "channel_id": d.get("channel_id"),
                "message_id": d.get("message_id"),
                "guild_id": d.get("guild_id"),
                "emoji": d.get("emoji"),
                "payload": d
            },
            Events.MESSAGE_REACTION_REMOVE: lambda d: {
                "user_id": d.get("user_id"),
                "channel_id": d.get("channel_id"),
                "message_id": d.get("message_id"),
                "guild_id": d.get("guild_id"),
                "emoji": d.get("emoji"),
                "payload": d
            },

            # Channel
            Events.CHANNEL_CREATE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
                "name": d.get("name"),
                "payload": d
            },
            Events.CHANNEL_UPDATE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
                "name": d.get("name"),
                "payload": d
            },
            Events.CHANNEL_DELETE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
                "payload": d
            },

            Events.CONVERSATION_SUMMARY_UPDATE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
                "text": d.get("summary", []).get("text"),
                "last_message_id": d.get("summary", []).get("last_message_id"),
                "message_count": d.get("summary", []).get("message_count"),
                "updated_at": d.get("summary", []).get("updated_at"),
                "payload": d
            },

            # Typing
            Events.TYPING_START: lambda d: {
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "user_id": d.get("user_id"),
                "timestamp": d.get("timestamp"),
                "payload": d
            },

            # Presence
            Events.PRESENCE_UPDATE: lambda d: {
                "user_id": d["user"].get("id"),
                "status": d.get("status"),
                "activities": d.get("activities"),
                "guild_id": d.get("guild_id"),
                "payload": d
            },

            # Voice
            Events.VOICE_STATE_UPDATE: lambda d: {
                "guild_id": d.get("guild_id"),
                "channel_id": d.get("channel_id"),
                "user_id": d.get("user_id"),
                "session_id": d.get("session_id"),
                "payload": d
            },
            Events.VOICE_SERVER_UPDATE: lambda d: {
                "guild_id": d.get("guild_id"),
                "endpoint": d.get("endpoint"),
                "token": d.get("token"),
                "payload": d
            },

            # Interaction
            Events.INTERACTION_CREATE: lambda d: {
                "interaction_id": d.get("id"),
                "interaction_token": d.get("token"),
                "cmd_type": d.get("type"),
                "guild_id": d.get("guild_id"),
                "channel_id": d.get("channel_id"),
                "user": d.get("member", {}).get("user"),
                "user_id": d.get("member", {}).get("user", {}).get("id"),
                "username": d.get("member", {}).get("user", {}).get("username"),
                "options": d.get("data", {}).get("options"),
                "values": [value.get("value") for value in d.get("data", {}).get("options", [])],
                "roles": d.get("member", []).get("roles", []),
                "payload": d,
            },

            # Invite
            Events.INVITE_CREATE: lambda d: {
                "code": d.get("code"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "inviter": d.get("inviter"),
                "payload": d
            },
            Events.INVITE_DELETE: lambda d: {
                "code": d.get("code"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "payload": d
            },

            # Webhooks
            Events.WEBHOOKS_UPDATE: lambda d: {
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "payload": d
            },
        }

    async def handle_events(self, response_json):
        response_event = response_json["t"]
        response_data = response_json["d"]
        sequence = response_json.get("t", None)
            
        self.logger.debug(f"Debug: Event sent by discord is {response_event}")

        if sequence is not None:
            self.session.sequence = sequence

        if response_event in self.dispatch_map and response_event != Events.INTERACTION_CREATE:
            payload = self.dispatch_map[response_event](response_data)
            await self.emit(response_event, **payload)
            
        elif response_event == Events.INTERACTION_CREATE:
            data = response_data["data"]
            if response_data.get("guild_id"):
                event = f"{Events.INTERACTION_CREATE}:{data["name"]}:{response_data["guild_id"]}"
            else:
                event = f"{Events.INTERACTION_CREATE}:{data["name"]}"

            payload = self.dispatch_map[response_event](response_data)
            
            await self.emit(event, **payload)
            await self.emit(response_event, **payload)
        else:
            self.logger.info(f"Event sent by discord is undefined {response_event}")