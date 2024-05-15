from enum import Enum

class UserStatusEnum(str, Enum):
    UNCONFIRMED = 'unconfirmed'
    CONFIRMED = 'confirmed'
    BANNED = 'banned'
