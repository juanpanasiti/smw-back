from enum import Enum


class SortableCreditCardFieldsEnum(str, Enum):
    # Basics
    ID = 'account_id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    # Owns
    ALIAS = 'alias'
    LIMIT = 'limit'
    NEXT_CLOSING_DATE = 'next_closing_date'
    NEXT_EXPIRING_DATE = 'next_expiring_date'


class SortableExpenseFieldsEnum(str, Enum):
    # Basics
    ID = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    # Owns
    TITLE = 'title'
    CC_NAME = 'cc_name'
    ACQUIRED_AT = 'acquired_at'
    AMOUNT = 'amount'
    TYPE = 'type'
    FIRST_PAYMENT_DATE = 'first_payment_date'
    STATUS = 'status'
    ACCOUNT_ID = 'account_id'


class SortablePaymentFieldsEnum(str, Enum):
    # Basics
    ID = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    # Owns
    AMOUNT = 'amount'
    STATUS = 'status'
    EXPENSE_ID = 'expense_id'
    NO_INSTALLMENT = 'no_installment'
    PERIOD = 'period'
