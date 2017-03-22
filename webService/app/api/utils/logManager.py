from functools import wraps
from bottle import request, response

import logging

from api.constants.index import LOG_MSG_DISABLING, LOG_MSG_ENABLING, LOG_MSG_UNKNOWN

file_handler = logging.FileHandler('../webService_logs.log')
formatter = logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


class LogManager:
    active = True
    logger = logging.getLogger('myApp')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    @classmethod
    def disable_logger(cls):
        if cls.active:
            cls.active = False
            cls.logger.info(LOG_MSG_DISABLING)

    @classmethod
    def enable_logger(cls):
        if not cls.active:
            cls.active = True
            cls.logger.info(LOG_MSG_ENABLING)

    @classmethod
    def info_log(cls, message=LOG_MSG_UNKNOWN):
        if cls.active:
            cls.logger.info(message)

    @classmethod
    def error_log(cls, message=LOG_MSG_UNKNOWN):
        if cls.active:
            cls.logger.error(message)

    @classmethod
    def warning_log(cls, message=LOG_MSG_UNKNOWN):
        if cls.active:
            cls.logger.warning(message)

    @classmethod
    def critical_log(cls, message=LOG_MSG_UNKNOWN):
        if cls.active:
            cls.logger.critical(message)

    @classmethod
    def debug_log(cls, message=LOG_MSG_UNKNOWN):
        if cls.active:
            cls.logger.debug(message)

    @classmethod
    def log_to_logger(cls, fn):
        """
        Wrap a Bottle request so that a log line is emitted after it's handled.
        """

        @wraps(fn)
        def _log_to_logger(*args, **kwargs):
            actual_response = fn(*args, **kwargs)

            if cls.active:
                cls.logger.info('Bottle -- %s %s %s %s' % (request.remote_addr,
                                                           request.method,
                                                           request.url.split("?")[0],
                                                           response.status))
            return actual_response

        return _log_to_logger
