from bottle import request
from bottle import post, get

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess

from api.constants.index import ErrorMessage, POSITIONS_TABLE


@post('/users/<user_id>/positions')
def creation_handler(user_id):
    """Handles user creation"""
    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        position = body['position']

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    try:
        dbaccess = SqliteDbAccess.create_service()
        position = dbaccess.insert(table=POSITIONS_TABLE,
                                   params={"position": position, "user": user_id},
                                   get_last_attribute=True)
    except SqliteDbAccess.Errors as e:
        return json_error_return()

    return json_success_return(position)


@get('/users/<user_id>/positions')
def list_positions_handler(user_id):
    """Handles listing of a user's positions"""

    dbaccess = SqliteDbAccess.create_service()
    positions = dbaccess.get(table=POSITIONS_TABLE, w_filter=("user =" + user_id))

    if positions:
        return json_success_return(positions)

    # TODO separate case user doesn't exist
    return json_error_return(ErrorMessage.NO_USER_OR_POSITION)


@get('/users/<user_id>/positions/last')
def show_last_position_handler(user_id):
    """Handles showing the last recorded position of a user"""

    dbaccess = SqliteDbAccess.create_service()
    w_filter = "user =" + user_id + " ORDER BY id DESC LIMIT 1"
    position = dbaccess.get(table=POSITIONS_TABLE, w_filter=w_filter, multiple=False)

    if position:
        return json_success_return(position)

    # TODO separate case user doesn't exist
    return json_error_return(ErrorMessage.NO_USER_OR_POSITION)
