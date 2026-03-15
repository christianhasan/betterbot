class Intents:
    default = 53575421
    all = 53608447

class CommandTypes:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9 # Can be user or role
    NUMBER = 10
    ATTACHMENT = 11

class ResponseTypes:
    RETRY_NOW = "RETRY_NOW"
    RETRY_DELAY = "RETRY_WITH_DELAY"
    SUCCESS = "SUCCESS"
    FAILED = "ATTEMPT_FAILED"
    CONNECTION_FAILED = "FAILED_DUE_TO_CONNECTION_ISSUES"