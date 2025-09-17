from ...shared.exception_base import ExceptionBase


class ExpenseStatusException(ExceptionBase):
    '''Exception raised for invalid expense status transitions.'''

    def __init__(self, message: str):
        super().__init__(message)
        self.code = 'EXPENSE_STATUS_EXCEPTION'


class ExpenseInvalidOperation(ExceptionBase):
    '''Exception raised for invalid expense operations.'''

    def __init__(self, message: str):
        super().__init__(message)
        self.code = 'EXPENSE_INVALID_OPERATION'


class ExpenseNotImplementedOperation(ExceptionBase):
    '''Exception raised for unimplemented expense operations.'''
    DEFAULT_MESSAGE = 'This operation is not implemented for this expense type.'

    def __init__(self, message: str = DEFAULT_MESSAGE):
        super().__init__(message)
        self.code = 'EXPENSE_NOT_IMPLEMENTED_OPERATION'
