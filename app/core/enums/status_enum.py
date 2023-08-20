from enum import Enum


class StatusEnum(str, Enum):
    UNCONFIRMED = 'unconfirmed'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    CANCELED = 'canceled'
