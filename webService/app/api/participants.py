from bottle import request
from bottle import post, get, delete

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess

from api.constants.index import ErrorMessage, CONVERSATIONS_MESSAGE_NAME
from api.constants.index import CONVERSATIONS_TABLE, CONVERSATION_PARTICIPANTS_TABLE


@get('/conversations/<conversation_id>/participants')
def list_conversation_participants_handler(conversation_id):
    """Handles the listing of participants in a conversation"""

    dbaccess = SqliteDbAccess.create_service()
    conversation = dbaccess.get(table=CONVERSATIONS_TABLE, w_filter=("id =" + conversation_id))

    if conversation:
        params = {
            "user":
                {
                    "attributes": ["id", "username"],
                    "join": "id"
                },
            "conversation_participant":
                {
                    "attributes": [],
                    "join": "user"
                }
        }
        w_filter = "conversation_participant.conversation =" + conversation_id

        participants = dbaccess.get_join(params=params, w_filter=w_filter)

        return json_success_return(participants)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=CONVERSATIONS_MESSAGE_NAME))

    pass


@post('/conversations/<conversation_id>/participants')
def create_conversation_participant_handler(conversation_id):
    """Add a participant to a conversation"""
    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        user_id = body['user_id']

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    try:
        dbaccess = SqliteDbAccess.create_service()
        dbaccess.insert(table=CONVERSATION_PARTICIPANTS_TABLE,
                        dict={"conversation": conversation_id, "user": user_id})
    except SqliteDbAccess.Errors as e:
        return json_error_return(ErrorMessage.USER_IN_CONVERSATION)

    return json_success_return()


@delete('/conversations/<conversation_id>/participants/<user_id>')
def delete_conversation_participant_handler(conversation_id, user_id):
    """Remove a participant from a conversation"""

    dbaccess = SqliteDbAccess.create_service(main_table=CONVERSATION_PARTICIPANTS_TABLE)
    participants = dbaccess.get(w_filter=("conversation =" + conversation_id + " AND user =" + user_id))
    if participants:
        try:
            dbaccess.delete(w_filter=("conversation =" + conversation_id + " AND user =" + user_id))
        except SqliteDbAccess.Errors as e:
            return json_error_return()

        return json_success_return()

    return json_error_return(ErrorMessage.USER_NOT_IN_CONVERSATION)
