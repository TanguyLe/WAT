from bottle import request, route
from bottle import post, get
from time import sleep

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess
from api.utils.index import WebsocketWrapper

from api.constants.index import ErrorMessage, POSITIONS_TABLE, USERS_TABLE, USERS_MESSAGE_NAME


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

        position = str(body['position'])

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    try:
        dbaccess = SqliteDbAccess.create_service()
        position = dbaccess.insert(table=POSITIONS_TABLE,
                                   params={"position": position, "user": user_id},
                                   get_last_attribute=True)
    except SqliteDbAccess.Error as e:
        return json_error_return(getattr(ErrorMessage, e.type).format(error=e))

    return json_success_return(position)


@get('/users/<user_id>/positions')
def list_positions_handler(user_id):
    """Handles listing of a user's positions"""

    dbaccess = SqliteDbAccess.create_service()
    user = dbaccess.get(table=USERS_TABLE, w_filter=("id =" + user_id))

    if user:
        positions = dbaccess.get(table=POSITIONS_TABLE, w_filter=("user =" + user_id))

        if positions:
            return json_success_return(positions)
        return json_error_return(ErrorMessage.NO_POSITION)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))


@get('/users/<user_id>/positions/last')
def show_last_position_handler(user_id):
    """Handles showing the last recorded position of a user"""

    dbaccess = SqliteDbAccess.create_service()
    user = dbaccess.get(table=USERS_TABLE, w_filter=("id =" + user_id))

    if user:
        w_filter = "user =" + user_id + " ORDER BY id DESC LIMIT 1"
        position = dbaccess.get(table=POSITIONS_TABLE, w_filter=w_filter, multiple=False)

        if position:
            return json_success_return(position)
        return json_error_return(ErrorMessage.NO_POSITION)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))


@route('/users/<user_id>/positionsSender')
def handle_position_setting(user_id):
    """Websocket implementation to record positions"""

    wsoc = WebsocketWrapper.create_service()

    while True:
        try:
            position = wsoc.receive()
            if position:
                dbaccess = SqliteDbAccess.create_service()
                dbaccess.insert(table=POSITIONS_TABLE,
                                params={"position": str(position), "user": user_id},
                                get_last_attribute=True)
        except WebsocketWrapper.Error:
            break

@route('/users/<user_id>/positionsGetter')
def handle_position_getting(user_id):
    """Websocket implementation to listen to positions"""
    w_filter = "user =" + user_id + " ORDER BY id DESC LIMIT 1"
    current_position = None

    wsoc = WebsocketWrapper.create_service()

    while True:
        try:
            dbaccess = SqliteDbAccess.create_service()
            position = dbaccess.get(table=POSITIONS_TABLE, w_filter=w_filter, multiple=False)
            if position and position["position"] != current_position:
                current_position = position["position"]
                wsoc.send(position["position"])
            sleep(1)
        except WebsocketWrapper.Error:
            break
