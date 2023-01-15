from enum import Enum


# here is the types of a respond

class TypesOfResponse(Enum):
    INITIALIZE = 1
    SEND_MSG = 2
    REQUEST_USERS_LIST = 3
    INCOMING_MESSAGE = 4
    SUCCESS = 5
    GETTING_USERS = 6
    USER_CONNECTED = 7
    USER_DISCONNECTED = 8
    ERROR = 9


class TypesOfSuccess(Enum):
    INITIALIZATION = 1
    MSG_SEND = 2