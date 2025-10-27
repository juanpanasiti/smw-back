from .base_http_exception import BaseHTTPException


class InternalServerError(BaseHTTPException):
    description = 'Unhadled error.'
    status_code = 500
    default_message = 'Unhandled error, contact the sysadmin'
    exception_code = 'INTERNAL_SERVER_ERROR'

    def __init__(self, message: str = None) -> None:
        super().__init__(message or self.default_message)


class NotImplemented(BaseHTTPException):
    description = 'Service not implemented yet.'
    status_code = 501
    exception_code = 'NOT_IMPLEMENTED'


class ServiceUnavailable(BaseHTTPException):
    description = 'Service is not available.'
    status_code = 503
    exception_code = 'SERVICE_UNAVAILABLE'

