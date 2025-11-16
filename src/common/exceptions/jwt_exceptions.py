from .base_exception import BaseException
from ..error_codes import JWT_EXPIRED, JWT_INVALID_SIGNATURE, JWT_INVALID


class JWTExpiredError(BaseException):
    """
    Exception raised when a JWT token has expired.

    Attributes:
        message (str): Human-readable error message.
        code (str): Error code representing the expired token error.
    """

    def __init__(self, message: str = 'Token has expired', code: str = JWT_EXPIRED):
        super().__init__(message=message, code=code)


class JWTInvalidSignatureError(BaseException):
    """
    Exception raised when a JWT token's signature is invalid or has been tampered with.

    Attributes:
        message (str): Human-readable error message.
        code (str): Error code representing the invalid signature error.
    """

    def __init__(self, message: str = 'Token signature is invalid', code: str = JWT_INVALID_SIGNATURE):
        super().__init__(message=message, code=code)


class JWTInvalidError(BaseException):
    """
    Exception raised when a JWT token is otherwise invalid or malformed.

    Attributes:
        message (str): Human-readable error message.
        code (str): Error code representing a generic invalid token error.
    """

    def __init__(self, message: str = 'Token is invalid', code: str = JWT_INVALID):
        super().__init__(message=message, code=code)
