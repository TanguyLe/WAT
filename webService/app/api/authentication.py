from bottle import request
from bottle import post

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess

from api.constants.index import ErrorMessage, USERS_TABLE, USERS_MESSAGE_NAME


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

        username = body['username']
        password = body['password']

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    dbaccess = SqliteDbAccess.create_service()
    user = dbaccess.get(table=USERS_TABLE, w_filter=("username =" + username))
    if user:
        if user['password'] == password:
            # TODO Of course new things will be necessary there
            return json_success_return({'loginKey': 'Ok'})
        return json_error_return(ErrorMessage.PASSWORD)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))
