from .base_http_exception import BaseHTTPException


class InternalServerError(BaseHTTPException):
    description = 'Unhadled error.'
    status_code = 500
    default_message = 'Unhandled error, contact the sysadmin'

    def __init__(self, message: str = None) -> None:
        super().__init__(message or self.default_message)


class NotImplemented(BaseHTTPException):
    description = 'Service not implemented yet.'
    status_code = 501


class ServiceUnavailable(BaseHTTPException):
    description = 'Service is not available.'
    status_code = 503
