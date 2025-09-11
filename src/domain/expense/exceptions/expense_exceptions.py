from ...shared.exception_base import ExceptionBase


class ExpenseStatusException(ExceptionBase):
    '''Exception raised for invalid expense status transitions.'''

    def __init__(self, message: str):
        super().__init__(message)
        self.code = 'EXPENSE_STATUS_EXCEPTION'
