from enum import Enum


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
