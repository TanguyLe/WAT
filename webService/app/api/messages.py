from bottle import request
from bottle import post, put, get, delete

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess

from api.constants.index import ErrorMessage, CONVERSATIONS_MESSAGE_NAME, MESSAGES_MESSAGE_NAME
from api.constants.index import CONVERSATIONS_TABLE, MESSAGES_TABLE


@get('/conversations/<conversation_id>/messages')
def list_conversations_handler(conversation_id):
    """Handles listing of conversation messages"""

    dbaccess = SqliteDbAccess.create_service()
    conversation = dbaccess.get(table=CONVERSATIONS_TABLE, w_filter=("id =" + conversation_id))
    if conversation:
        messages = dbaccess.get(table=MESSAGES_TABLE, w_filter=("conversation =" + conversation_id))
        return json_success_return(messages)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=CONVERSATIONS_MESSAGE_NAME))


@post('/conversations/<conversation_id>/messages')
def create_conversation_handler(conversation_id):
    """Handles message creation"""
    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        user_id = body['user_id']
        content = body['content']

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    try:
        dbaccess = SqliteDbAccess.create_service()
        message = dbaccess.insert(table=MESSAGES_TABLE,
                                  params={"content": content, "conversation": conversation_id, "user": user_id},
                                  get_last_attribute=True)
    except SqliteDbAccess.Errors as e:
        return json_error_return()

    return json_success_return(message)


@put('/messages/<msg_id>')
def update_message_content_handler(msg_id):
    """Handles message content update"""

    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        content = body["content"]

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    dbaccess = SqliteDbAccess.create_service(main_table=MESSAGES_TABLE)
    message = dbaccess.get(w_filter=("id =" + msg_id))

    if message:
        try:
            dbaccess.update(s_filter=("content ='" + content + "'"), w_filter=("id =" + msg_id))
        except SqliteDbAccess.Errors as e:
            return json_error_return()

        return json_success_return()

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=MESSAGES_MESSAGE_NAME))


@delete('/messages/<msg_id>')
def delete_message_handler(msg_id):
    """Handles message deletion"""

    dbaccess = SqliteDbAccess.create_service(main_table=MESSAGES_TABLE)
    message = dbaccess.get(w_filter=("id =" + msg_id))

    if message:
        try:
            dbaccess.delete(w_filter="id =" + msg_id)
        except SqliteDbAccess.Errors as e:

            return json_error_return()

        return json_success_return()

    # TODO separate case user doesn't exist
    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=MESSAGES_MESSAGE_NAME))
