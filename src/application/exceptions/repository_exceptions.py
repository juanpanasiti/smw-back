from src.common.exceptions.base_exception import BaseException

class BaseRepoException(BaseException):
    default_message = None

    def __init__(self, message: str = "", code: str | None = None) -> None:
        message = message or self.default_message or ""
        super().__init__(message=message, code=code)


class NotFoundError(BaseRepoException):
    default_message = 'Resource not found.'


class UniqueFieldException(BaseRepoException):
    default_message = 'Some field is duplicated on DB'


class DatabaseError(BaseRepoException):
    default_message = 'Something went wrong with a database operation'


class MatchPasswordException(BaseRepoException):
    default_message = "Password doesn't match."
