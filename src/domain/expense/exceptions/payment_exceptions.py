from ...shared.exception_base import ExceptionBase


class PaymentNotFoundInExpenseException(ExceptionBase):
    '''Exception raised when a payment is not found in an expense.'''

    def __init__(self, message: str):
        super().__init__(message)
        self.code = 'PAYMENT_NOT_FOUND_IN_EXPENSE_EXCEPTION'
