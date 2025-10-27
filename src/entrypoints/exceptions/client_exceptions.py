from .base_http_exception import BaseHTTPException


class BadRequest(BaseHTTPException):
    description = 'Something is wrong with the request'
    status_code = 400
    exception_code = 'BAD_REQUEST'


class Unauthorized(BaseHTTPException):
    description = 'Must be logged in.'
    status_code = 401
    exception_code = 'UNAUTHORIZED'


class Forbidden(BaseHTTPException):
    status_code = 403
    description = 'Have no access to this resource.'
    exception_code = 'FORBIDDEN'


class NotFound(BaseHTTPException):
    description = 'Resource not found.'
    status_code = 404
    exception_code = 'NOT_FOUND'
