class BaseAppException(Exception):
    default_message = None

    def __init__(self, message: str) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)

# Service exceptions


class NotFoundError(BaseAppException):
    default_message = 'Resource not found.'
