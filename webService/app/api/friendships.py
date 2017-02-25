from bottle import request
from bottle import post, get, delete

from api.utils.index import json_success_return, json_error_return
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, USERS_MESSAGE_NAME, FRIENDSHIPS_MESSAGE_NAME
from api.constants.index import USERS_TABLE, FRIENDSHIPS_TABLE


@get('/users/<user_id>/friends')
def list_friends_handler(user_id):
    """Handles the listing of a user's friends"""

    dbaccess = sqliteDbAccess.create_service()
    user = dbaccess.get(table=USERS_TABLE, w_filter=("id =" + user_id))
    if user:
        params = {
            "user":
                {
                    "attributes": ["id", "username"],
                    "join": "id"
                },
            "friendship":
                {
                    "attributes": [],
                    "join": "firstFriend"
                }
        }
        w_filter = "friendship.secondFriend =" + user_id

        users = dbaccess.get_join(params=params, w_filter=w_filter)

        return json_success_return(users)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))


@post('/users/<user_id>/friends')
def creation_handler(user_id):
    """Handles friendship creation"""

    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        friend_id = body['user_id']

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    try:
        dbaccess = sqliteDbAccess.create_service()
        w_filter = "firstFriend =" + str(friend_id) + " AND secondFriend =" + str(user_id)
        friendship = dbaccess.get(table=FRIENDSHIPS_TABLE, w_filter=w_filter)
        if friendship:
            return json_error_return(ErrorMessage.EXISTS_ALREADY.format(name=FRIENDSHIPS_MESSAGE_NAME))

        dbaccess.insert(table=FRIENDSHIPS_TABLE, dict={"firstFriend": user_id, "secondFriend": friend_id})
        dbaccess.insert(table=FRIENDSHIPS_TABLE, dict={"firstFriend": friend_id, "secondFriend": user_id})
    except sqliteDbAccess.Errors as e:
        return json_error_return()

    return json_success_return()


@delete('/users/<user_id>/friends/<friend_id>')
def deletion_handler(user_id, friend_id):
    """Handles friendship deletion"""

    dbaccess = sqliteDbAccess.create_service(main_table=FRIENDSHIPS_TABLE)
    w_filter1 = "firstFriend =" + friend_id + " AND secondFriend =" + user_id
    w_filter2 = "firstFriend =" + user_id + " AND secondFriend =" + friend_id
    friendship = dbaccess.get(w_filter=w_filter1)

    if friendship:
        try:
            dbaccess.delete(w_filter=w_filter1)
            dbaccess.delete(w_filter=w_filter2)
        except sqliteDbAccess.Errors as e:
            return json_error_return()

        return json_success_return()

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=FRIENDSHIPS_MESSAGE_NAME))
