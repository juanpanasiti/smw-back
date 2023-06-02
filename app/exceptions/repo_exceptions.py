class BaseRepoException(Exception):
    default_message = None

    def __init__(self, message: str) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(BaseRepoException):
    default_message = 'Resource not found.'


class DatabaseError(BaseRepoException):
    default_message = 'Something went wrong with a database operation'
