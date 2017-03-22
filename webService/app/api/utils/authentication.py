import jwt
import datetime

from api.utils.index import LogManager

from api.constants.index import HASH_ALGORITHM, HASH_SECRET, DATETIME_OFFSET_FORMAT, ErrorMessage
from api.constants.index import LOG_AUTHENTICATION


def authenticate_user(password=None):
    try:
        decoded = jwt.decode(password.encode(), HASH_SECRET, algorithms=[HASH_ALGORITHM])
    except jwt.exceptions.DecodeError:
        LogManager.error_log(LOG_AUTHENTICATION + ErrorMessage.INCORRECT_TOKEN)
        return ErrorMessage.INCORRECT_TOKEN

    try:
        expiration = datetime.datetime.strptime(decoded['expiration'], DATETIME_OFFSET_FORMAT)
    except ValueError:
        LogManager.error_log(LOG_AUTHENTICATION + ErrorMessage.INCORRECT_TOKEN)
        return ErrorMessage.INCORRECT_TOKEN

    if expiration < datetime.datetime.now():
        LogManager.error_log(LOG_AUTHENTICATION + ErrorMessage.TIMEOUT)
        return ErrorMessage.TIMEOUT

    LogManager.info_log(LOG_AUTHENTICATION + "Authentication successful")
    return None
