from .app_exceptions import BaseAppException


class NotFoundError(BaseAppException):
    default_message = 'Resource not found.'


class UniqueFieldException(BaseAppException):
    default_message = 'Some field is duplicated on DB'


class DatabaseError(BaseAppException):
    default_message = 'Something went wrong with a database operation'


class MatchPasswordException(BaseAppException):
    default_message = 'Password doesn\'t match.'
