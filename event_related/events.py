class Events:
    EVERYTHING = "listen_to_everything"  # You can subscribe to this if you want to listen to all events.

    # Lifecycle
    BOT_READY = "READY"  # Bot is ready

    # Guild
    GUILD_CREATE = "GUILD_CREATE"  # Guild added
    GUILD_UPDATE = "GUILD_UPDATE"  # Guild updated
    GUILD_DELETE = "GUILD_DELETE"  # Guild removed
    GUILD_ROLE_CREATE = "GUILD_ROLE_CREATE"  # Role created
    GUILD_ROLE_UPDATE = "GUILD_ROLE_UPDATE"  # Role updated
    GUILD_ROLE_DELETE = "GUILD_ROLE_DELETE"  # Role deleted
    GUILD_BAN_ADD = "GUILD_BAN_ADD"  # User banned
    GUILD_BAN_REMOVE = "GUILD_BAN_REMOVE"  # User unbanned
    GUILD_EMOJIS_UPDATE = "GUILD_EMOJIS_UPDATE"  # Emojis updated
    GUILD_STICKERS_UPDATE = "GUILD_STICKERS_UPDATE"  # Stickers updated
    GUILD_INTEGRATIONS_UPDATE = "GUILD_INTEGRATIONS_UPDATE"  # Integrations updated
    GUILD_SCHEDULED_EVENT_CREATE = "GUILD_SCHEDULED_EVENT_CREATE"  # Event created
    GUILD_SCHEDULED_EVENT_UPDATE = "GUILD_SCHEDULED_EVENT_UPDATE"  # Event updated
    GUILD_SCHEDULED_EVENT_DELETE = "GUILD_SCHEDULED_EVENT_DELETE"  # Event deleted

    # Channel
    CHANNEL_CREATE = "CHANNEL_CREATE"  # Channel created
    CHANNEL_UPDATE = "CHANNEL_UPDATE"  # Channel updated
    CHANNEL_DELETE = "CHANNEL_DELETE"  # Channel deleted
    CHANNEL_PINS_UPDATE = "CHANNEL_PINS_UPDATE"  # Pins updated

    # Thread
    THREAD_CREATE = "THREAD_CREATE"  # Thread created
    THREAD_UPDATE = "THREAD_UPDATE"  # Thread updated
    THREAD_DELETE = "THREAD_DELETE"  # Thread deleted
    THREAD_LIST_SYNC = "THREAD_LIST_SYNC"  # Thread list synced
    THREAD_MEMBER_UPDATE = "THREAD_MEMBER_UPDATE"  # Thread member updated
    THREAD_MEMBERS_UPDATE = "THREAD_MEMBERS_UPDATE"  # Thread members updated

    # Member
    GUILD_MEMBER_ADD = "GUILD_MEMBER_ADD"  # Member added
    GUILD_MEMBER_REMOVE = "GUILD_MEMBER_REMOVE"  # Member removed
    GUILD_MEMBER_UPDATE = "GUILD_MEMBER_UPDATE"  # Member updated
    
    # Message
    MESSAGE_CREATE = "MESSAGE_CREATE"  # Message created
    MESSAGE_UPDATE = "MESSAGE_UPDATE"  # Message updated
    MESSAGE_DELETE = "MESSAGE_DELETE"  # Message deleted
    MESSAGE_DELETE_BULK = "MESSAGE_DELETE_BULK"  # Messages bulk deleted

    # Reaction
    MESSAGE_REACTION_ADD = "MESSAGE_REACTION_ADD"  # Reaction added
    MESSAGE_REACTION_REMOVE = "MESSAGE_REACTION_REMOVE"  # Reaction removed
    MESSAGE_REACTION_REMOVE_ALL = "MESSAGE_REACTION_REMOVE_ALL"  # All reactions removed
    MESSAGE_REACTION_REMOVE_EMOJI = "MESSAGE_REACTION_REMOVE_EMOJI"  # Emoji reactions removed

    # Presence / Typing / User
    PRESENCE_UPDATE = "PRESENCE_UPDATE"  # Presence changed
    TYPING_START = "TYPING_START"  # Typing started
    USER_UPDATE = "USER_UPDATE"  # User updated

    # Voice
    VOICE_STATE_UPDATE = "VOICE_STATE_UPDATE"  # Voice state updated
    VOICE_SERVER_UPDATE = "VOICE_SERVER_UPDATE"  # Voice server updated

    # Interaction / Application
    INTERACTION_CREATE = "INTERACTION_CREATE"  # Interaction created
    APPLICATION_COMMAND_CREATE = "APPLICATION_COMMAND_CREATE"  # Command created
    APPLICATION_COMMAND_UPDATE = "APPLICATION_COMMAND_UPDATE"  # Command updated
    APPLICATION_COMMAND_DELETE = "APPLICATION_COMMAND_DELETE"  # Command deleted
    APPLICATION_COMMAND_PERMISSIONS_UPDATE = "APPLICATION_COMMAND_PERMISSIONS_UPDATE"  # Command permissions updated

    # Invite
    INVITE_CREATE = "INVITE_CREATE"  # Invite created
    INVITE_DELETE = "INVITE_DELETE"  # Invite deleted

    # Auto-Moderation
    AUTO_MODERATION_RULE_CREATE = "AUTO_MODERATION_RULE_CREATE"  # Rule created
    AUTO_MODERATION_RULE_UPDATE = "AUTO_MODERATION_RULE_UPDATE"  # Rule updated
    AUTO_MODERATION_RULE_DELETE = "AUTO_MODERATION_RULE_DELETE"  # Rule deleted
    AUTO_MODERATION_ACTION_EXECUTION = "AUTO_MODERATION_ACTION_EXECUTION"  # Action executed
    AUTO_MODERATION_INCIDENT_CREATE = "AUTO_MODERATION_INCIDENT_CREATE"  # Incident created
    AUTO_MODERATION_INCIDENT_UPDATE = "AUTO_MODERATION_INCIDENT_UPDATE"  # Incident updated
    AUTO_MODERATION_INCIDENT_DELETE = "AUTO_MODERATION_INCIDENT_DELETE"  # Incident deleted
    AUTO_MODERATION_MENTION_RAID_DETECTION = "AUTO_MODERATION_MENTION_RAID_DETECTION"  # Raid detected

    # Stage
    STAGE_INSTANCE_CREATE = "STAGE_INSTANCE_CREATE"  # Stage created
    STAGE_INSTANCE_DELETE = "STAGE_INSTANCE_DELETE"  # Stage deleted
    STAGE_INSTANCE_UPDATE = "STAGE_INSTANCE_UPDATE"  # Stage updated

    # Integration
    INTEGRATION_CREATE = "INTEGRATION_CREATE"  # Integration created
    INTEGRATION_UPDATE = "INTEGRATION_UPDATE"  # Integration updated
    INTEGRATION_DELETE = "INTEGRATION_DELETE"  # Integration deleted

    # Webhook
    WEBHOOKS_UPDATE = "WEBHOOKS_UPDATE"  # Webhooks updated

    # Scheduled Event User
    GUILD_SCHEDULED_EVENT_USER_ADD = "GUILD_SCHEDULED_EVENT_USER_ADD"  # User added to event
    GUILD_SCHEDULED_EVENT_USER_REMOVE = "GUILD_SCHEDULED_EVENT_USER_REMOVE"  # User removed from event