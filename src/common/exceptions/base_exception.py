class BaseException(Exception):
    """
    Base class for all custom exceptions in the project.

    Accepts a descriptive message and an optional error code
    to facilitate error identification and handling.
    """

    def __init__(self, message: str = "", code: str | None = None):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message
