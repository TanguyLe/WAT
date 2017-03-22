import jwt
import datetime
from bottle import request
from bottle import post

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess

from api.constants.index import ErrorMessage, USERS_TABLE, USERS_MESSAGE_NAME
from api.constants.index import DATETIME_OFFSET_FORMAT, HASH_SECRET, HASH_ALGORITHM


@post('/login')
def login_handler():
    """Handles login"""
    try:

        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        username = str(body['username'])
        password = str(body['password'])

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    dbaccess = SqliteDbAccess.create_service()
    user = dbaccess.get(table=USERS_TABLE, w_filter=("username ='" + username + "'"), multiple=False)
    if user:
        if user['password'] == password:
            return json_success_return(
                {'token': jwt.encode({'expiration': (
                    datetime.datetime.today() + datetime.timedelta(minutes=60)).strftime(DATETIME_OFFSET_FORMAT)},
                                     HASH_SECRET,
                                     algorithm=HASH_ALGORITHM).decode()})
        return json_error_return(ErrorMessage.PASSWORD)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))
