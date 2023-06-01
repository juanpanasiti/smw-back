from enum import Enum


class StatusEnum(str, Enum):
    TO_CHECK = 'to_check'
    IN_PROGRESS = 'in_progress'
    REFUNDED = 'refunded'
    CANCELED = 'canceled'
    PAID = 'paid'
