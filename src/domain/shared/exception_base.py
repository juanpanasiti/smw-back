

class ExceptionBase(Exception):
    '''Base class for all exceptions in the application.'''
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.code: str = 'GENERIC_EXCEPTION'

    def __str__(self):
        return f'{self.code}: {self.message}'