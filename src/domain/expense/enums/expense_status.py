from enum import Enum


class ExpenseStatus(str, Enum):
    ACTIVE = 'active'
    PENDING = 'pending'
    FINISHED = 'finished'
    CANCELLED = 'cancelled'
