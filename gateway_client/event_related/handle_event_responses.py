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
                "user_id": d["user"].get("id"),
                "username": d["user"].get("username"),
                "guilds": d.get("guilds"),
                "session_id": d.get("session_id"),
                "payload": d,  # full raw payload
            },

            Events.SESSIONS_REPLACE: lambda d: {},

            # Guild
            Events.GUILD_CREATE: lambda d: {
                "guild_id": d.get("id"),
                "name": d.get("name"),
                "guild": d,
            },
            Events.GUILD_UPDATE: lambda d: {
                "guild_id": d.get("id"),
                "name": d.get("name"),
                "guild": d,
            },
            Events.GUILD_DELETE: lambda d: {
                "guild_id": d.get("id"),
                "unavailable": d.get("unavailable"),
            },

            # Member
            Events.GUILD_MEMBER_ADD: lambda d: {
                "guild_id": d.get("guild_id"),
                "user_id": d["user"]["id"],
                "username": d["user"]["username"],
                "member": d,
            },
            Events.GUILD_MEMBER_REMOVE: lambda d: {
                "guild_id": d.get("guild_id"),
                "user_id": d["user"]["id"],
                "username": d["user"]["username"],
                "member": d,
            },
            Events.GUILD_MEMBER_UPDATE: lambda d: {
                "guild_id": d.get("guild_id"),
                "user_id": d["user"]["id"],
                "username": d["user"]["username"],
                "member": d,
            },

            # Message
            Events.MESSAGE_CREATE: lambda d: {
                "message_id": d.get("id"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "user_id": d["author"]["id"],
                "username": d["author"]["username"],
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
            },
            Events.MESSAGE_REACTION_REMOVE: lambda d: {
                "user_id": d.get("user_id"),
                "channel_id": d.get("channel_id"),
                "message_id": d.get("message_id"),
                "guild_id": d.get("guild_id"),
                "emoji": d.get("emoji"),
            },

            # Channel
            Events.CHANNEL_CREATE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
                "name": d.get("name"),
                "channel": d,
            },
            Events.CHANNEL_UPDATE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
                "name": d.get("name"),
                "channel": d,
            },
            Events.CHANNEL_DELETE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
            },

            Events.CONVERSATION_SUMMARY_UPDATE: lambda d: {
                "channel_id": d.get("id"),
                "guild_id": d.get("guild_id"),
                "text": d.get("summary", []).get("text"),
                "last_message_id": d.get("summary", []).get("last_message_id"),
                "message_count": d.get("summary", []).get("message_count"),
                "updated_at": d.get("summary", []).get("updated_at")
            },

            # Typing
            Events.TYPING_START: lambda d: {
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "user_id": d.get("user_id"),
                "timestamp": d.get("timestamp"),
            },

            # Presence
            Events.PRESENCE_UPDATE: lambda d: {
                "user_id": d["user"].get("id"),
                "status": d.get("status"),
                "activities": d.get("activities"),
                "guild_id": d.get("guild_id"),
            },

            # Voice
            Events.VOICE_STATE_UPDATE: lambda d: {
                "guild_id": d.get("guild_id"),
                "channel_id": d.get("channel_id"),
                "user_id": d.get("user_id"),
                "session_id": d.get("session_id"),
                "voice_state": d,
            },
            Events.VOICE_SERVER_UPDATE: lambda d: {
                "guild_id": d.get("guild_id"),
                "endpoint": d.get("endpoint"),
                "token": d.get("token"),
            },

            # Interaction
            Events.INTERACTION_CREATE: lambda d: {
                "interaction_id": d.get("id"),
                "type": d.get("type"),
                "guild_id": d.get("guild_id"),
                "channel_id": d.get("channel_id"),
                "user": d.get("member", {}).get("user") or d.get("user"),
                "interaction": d,
            },

            # Invite
            Events.INVITE_CREATE: lambda d: {
                "code": d.get("code"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
                "inviter": d.get("inviter"),
            },
            Events.INVITE_DELETE: lambda d: {
                "code": d.get("code"),
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
            },

            # Webhooks
            Events.WEBHOOKS_UPDATE: lambda d: {
                "channel_id": d.get("channel_id"),
                "guild_id": d.get("guild_id"),
            },
        }

    async def handle_events(self, response_json):
        response_event = response_json["t"]
        response_data = response_json["d"]
        sequence = response_json.get("t", None)
            
        self.logger.debug(f"Debug: Event sent by discord is {response_event}")

        if sequence is not None:
            self.session.sequence = sequence

        if response_event in self.dispatch_map:
            payload = self.dispatch_map[response_event](response_data)
            await self.emit(response_event, **payload)
        else:
            self.logger.warning(f"Event sent by discord is undefined {response_event}")