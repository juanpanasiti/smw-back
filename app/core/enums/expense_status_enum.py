from enum import Enum


class ExpenseStatusEnum(str, Enum):
    ACTIVE = 'active'
    FINISHED = 'finished'
