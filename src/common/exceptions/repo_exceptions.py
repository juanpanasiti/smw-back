from .base_exception import BaseException
from ..error_codes import REPO_ERROR, REPO_NOT_FOUND


class RepositoryError(BaseException):
    """
    Exception raised for errors occurring in the repository layer.

    Inherits from BaseException and can include an optional error code
    for more specific error identification.
    """

    def __init__(self, message: str = 'An error occurred in the repository layer.', code: str = REPO_ERROR):
        super().__init__(message, code)


class RepoNotFoundError(BaseException):
    """
    Exception raised when a requested entity is not found in the repository.

    Inherits from BaseException and includes a specific error code for not found errors.
    """

    def __init__(self, message: str = 'The requested entity was not found.', code: str = REPO_NOT_FOUND):
        super().__init__(message, code)
