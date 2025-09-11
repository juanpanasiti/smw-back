from enum import Enum


class ExpenseType(str, Enum):
    PURCHASE = 'purchase'
    SUBSCRIPTION = 'subscription'
