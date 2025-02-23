import logging
from . import BaseHTTPException, InternalServerError


def handle_exceptions(func):
    logger = logging.getLogger(func.__module__)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseHTTPException as ex:
            logger.error(f'Error in function "{func.__name__}": {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(f'Unhandled exception in function "{func.__name__}": {ex}')
            logger.critical(ex.args)
            raise InternalServerError(ex.args, 'UNHANDLED_ERROR')
    return wrapper
