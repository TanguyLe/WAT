from bottle import request
from bottle import post, get, delete, put

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess

from api.constants.index import ErrorMessage, USERS_MESSAGE_NAME, CONVERSATIONS_MESSAGE_NAME, MESSAGES_TABLE
from api.constants.index import USERS_TABLE, CONVERSATION_PARTICIPANTS_TABLE, CONVERSATIONS_TABLE


@get('/users/<user_id>/conversations')
def list_conversations_handler(user_id):
    """Handles listing of the conversations of a user"""

    dbaccess = SqliteDbAccess.create_service()
    user = dbaccess.get(table=USERS_TABLE, w_filter=("id =" + user_id))

    if user:
        params = {
            "conversation":
                {
                    "attributes": ["id", "name"],
                    "join": "id"
                },
            "conversation_participant":
                {
                    "attributes": [],
                    "join": "conversation"
                }
        }
        w_filter = "conversation_participant.user =" + user_id

        conversations = dbaccess.get_join(params=params, w_filter=w_filter)

        return json_success_return(conversations)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))


@post('/users/<user_id>/conversations')
def create_conversation_handler(user_id):
    """Handles conversation creation"""

    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        conversation_name = body['convname']
        second_user_id = body['user_id']

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    try:
        dbaccess = SqliteDbAccess.create_service(main_table=CONVERSATION_PARTICIPANTS_TABLE)
        conversation = dbaccess.insert(table=CONVERSATIONS_TABLE,
                                       params={"name": conversation_name},
                                       get_last_attribute=True)

        dbaccess.insert(dict={"conversation": conversation["id"], "user": user_id})
        dbaccess.insert(dict={"conversation": conversation["id"], "user": second_user_id})
    except SqliteDbAccess.Errors as e:
        return json_error_return()

    return json_success_return(conversation)


@put('/conversations/<conversation_id>')
def update_conversation_name_handler(conversation_id):
    """Handles conversation name change"""

    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        conversation_name = body["convname"]

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    dbaccess = SqliteDbAccess.create_service(main_table=CONVERSATIONS_TABLE)
    conversation = dbaccess.get(w_filter=("id = " + conversation_id))

    if conversation:
        try:
            dbaccess.update(s_filter=("name = '" + conversation_name + "'"), w_filter=("id = " + conversation_id))
        except SqliteDbAccess.Errors as e:
            return json_error_return(ErrorMessage.EXISTS_ALREADY.format(name=CONVERSATIONS_MESSAGE_NAME))

        return json_success_return()

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=CONVERSATIONS_MESSAGE_NAME))


@delete('/conversations/<conversation_id>')
def delete_conversation_handler(conversation_id):
    """Handles conversation deletion"""

    dbaccess = SqliteDbAccess.create_service(main_table=CONVERSATIONS_TABLE)
    conversation = dbaccess.get(w_filter=("id = " + conversation_id))

    if conversation:
        try:
            w_filter = "conversation =" + conversation_id
            dbaccess.delete(table=CONVERSATION_PARTICIPANTS_TABLE, w_filter=w_filter, commit=False)
            dbaccess.delete(table=MESSAGES_TABLE, w_filter=w_filter, commit=False)
            dbaccess.delete(w_filter=("id =" + conversation_id))
        except SqliteDbAccess.Errors as e:
            return json_error_return()

        return json_success_return()

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=CONVERSATIONS_MESSAGE_NAME))
