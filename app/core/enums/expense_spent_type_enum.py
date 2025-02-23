from enum import Enum


class ExpenseSpentTypeEnum(str, Enum):
    BASIC = 'basic'
    SAVINGS = 'savings'
    LUXURY = 'luxury'
