class Endpoints:
    BASE_URL = "https://discord.com/api/v9/"

    # Interactions / Slash Commands
    INTERACTION_CALLBACK = lambda d: f"{Endpoints.BASE_URL}interactions/{d['interaction_id']}/{d['interaction_token']}/callback"
    INTERACTION_FOLLOWUP = lambda d: f"{Endpoints.BASE_URL}webhooks/{d['application_id']}/{d['interaction_token']}"
    INTERACTION_ORIGINAL_MESSAGE = lambda d: f"{Endpoints.BASE_URL}webhooks/{d['application_id']}/{d['interaction_token']}/messages/@original"
    INTERACTION_UPDATE_MESSAGE = lambda d: f"{Endpoints.BASE_URL}webhooks/{d['application_id']}/{d['interaction_token']}/messages/{d.get('message_id', '@original')}"

    # Application Commands
    APPLICATION_GLOBAL_COMMANDS = lambda d: f"{Endpoints.BASE_URL}applications/{d['application_id']}/commands"
    APPLICATION_COMMAND = lambda d: f"{Endpoints.BASE_URL}applications/{d['application_id']}/commands/{d['command_id']}"
    APPLICATION_GUILD_COMMANDS = lambda d: f"{Endpoints.BASE_URL}applications/{d['application_id']}/guilds/{d['guild_id']}/commands"
    APPLICATION_GUILD_COMMAND = lambda d: f"{Endpoints.BASE_URL}applications/{d['application_id']}/guilds/{d['guild_id']}/commands/{d['command_id']}"
    APPLICATION_COMMAND_PERMISSIONS = lambda d: f"{Endpoints.BASE_URL}applications/{d['application_id']}/guilds/{d['guild_id']}/commands/{d['command_id']}/permissions"

    # Channels
    CHANNEL_INFO = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}"
    CHANNEL_MESSAGES = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/messages"
    CHANNEL_MESSAGE = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/messages/{d['message_id']}"
    CHANNEL_REACTIONS = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/messages/{d['message_id']}/reactions/{d['emoji']}"
    CHANNEL_REACTION_USER = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/messages/{d['message_id']}/reactions/{d['emoji']}/{d['user_id']}"
    CHANNEL_BULK_DELETE_MESSAGES = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/messages/bulk-delete"
    CHANNEL_PINS = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/pins"
    CHANNEL_PIN = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/pins/{d['message_id']}"
    CHANNEL_TYPING = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/typing"

    # Threads
    THREAD_CREATE = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/messages/{d['message_id']}/threads"
    THREAD_MEMBERS_LIST = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/thread-members"
    THREAD_MEMBER_INFO = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/thread-members/{d['user_id']}"
    THREAD_ACTIVE_LIST = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/threads/active"

    # Guilds
    GUILD_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}"
    GUILD_MEMBERS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/members"
    GUILD_MEMBER_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/members/{d['user_id']}"
    GUILD_ROLES_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/roles"
    GUILD_ROLE_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/roles/{d['role_id']}"
    MEMBER_ROLE_ASSIGN = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/members/{d['user_id']}/roles/{d['role_id']}"
    GUILD_BANS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/bans"
    GUILD_BAN_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/bans/{d['user_id']}"
    GUILD_PRUNE_MEMBERS = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/prune"
    GUILD_CHANNELS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/channels"

    # Emojis
    GUILD_EMOJIS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/emojis"
    GUILD_EMOJI_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/emojis/{d['emoji_id']}"

    # Stickers
    GUILD_STICKERS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/stickers"
    GUILD_STICKER_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/stickers/{d['sticker_id']}"

    # Invites
    INVITE_INFO = lambda d: f"{Endpoints.BASE_URL}invites/{d['invite_code']}"
    CHANNEL_INVITES_LIST = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/invites"
    GUILD_INVITES_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/invites"

    # Webhooks
    CHANNEL_WEBHOOKS_LIST = lambda d: f"{Endpoints.BASE_URL}channels/{d['channel_id']}/webhooks"
    GUILD_WEBHOOKS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/webhooks"
    WEBHOOK_INFO = lambda d: f"{Endpoints.BASE_URL}webhooks/{d['webhook_id']}"
    WEBHOOK_INFO_WITH_TOKEN = lambda d: f"{Endpoints.BASE_URL}webhooks/{d['webhook_id']}/{d['webhook_token']}"

    # Users
    USER_ME = lambda d: f"{Endpoints.BASE_URL}users/@me"
    USER_INFO = lambda d: f"{Endpoints.BASE_URL}users/{d['user_id']}"
    USER_ME_GUILDS_LIST = lambda d: f"{Endpoints.BASE_URL}users/@me/guilds"
    USER_ME_GUILD_INFO = lambda d: f"{Endpoints.BASE_URL}users/@me/guilds/{d['guild_id']}"

    # Voice
    VOICE_STATE_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/voice-states/{d['user_id']}"

    # Scheduled Events
    SCHEDULED_EVENTS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/scheduled-events"
    SCHEDULED_EVENT_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/scheduled-events/{d['event_id']}"
    SCHEDULED_EVENT_USERS = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/scheduled-events/{d['event_id']}/users"

    # Stage Instances
    STAGE_INSTANCE_INFO = lambda d: f"{Endpoints.BASE_URL}stage-instances/{d['channel_id']}"

    # Audit Logs
    AUDIT_LOGS_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/audit-logs"

    # Auto Moderation Rules
    AUTO_MOD_RULES_LIST = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/auto-moderation/rules"
    AUTO_MOD_RULE_INFO = lambda d: f"{Endpoints.BASE_URL}guilds/{d['guild_id']}/auto-moderation/rules/{d['rule_id']}"