from enum import Enum


class ExpenseTypeEnum(str, Enum):
    PURCHASE = 'purchase'
    SUBSCRIPTION = 'subscription'
