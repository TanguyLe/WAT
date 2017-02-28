from bottle import request
from bottle import post, get, delete, route

from api.utils.index import json_success_return, json_error_return
from api.utils.index import SqliteDbAccess

from api.constants.index import ErrorMessage, USERS_TABLE, USERS_MESSAGE_NAME


@get('/users')
def list_user_handler():
    """Handles users listing"""

    dbaccess = SqliteDbAccess.create_service()
    users = dbaccess.get(table=USERS_TABLE)

    return json_success_return(users)


@get('/users/<user_id>')
def show_user_handler(user_id):
    """Handles single user show"""

    dbaccess = SqliteDbAccess.create_service()
    user = dbaccess.get(table=USERS_TABLE, w_filter=("id =" + user_id), multiple=False)

    if user:
        return json_success_return(user)

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))


@post('/users')
def create_user_handler():
    """Handles user creation"""

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

    try:
        dbaccess = SqliteDbAccess.create_service()
        user = dbaccess.insert(table=USERS_TABLE,
                               params={"username": username, "password": password},
                               get_last_attribute=True)
    except SqliteDbAccess.Error as e:
        if e.type == "INTEGRITY_ERROR":
            return json_error_return(ErrorMessage.EXISTS_ALREADY.format(name=USERS_MESSAGE_NAME))
        return json_error_return(getattr(ErrorMessage, e.type).format(error=e))

    return json_success_return(user)


@route('/users/<user_id>', 'PATCH')
def update_username_or_password_handler(user_id):
    """Handles changing username or password"""

    try:
        try:
            body = request.json
        except:
            raise ValueError

        if body is None:
            raise ValueError

        keys = list(body.keys())
        keys = [str(elem) for elem in keys]

    except ValueError:
        return json_error_return(ErrorMessage.VALUE)

    except KeyError:
        return json_error_return(ErrorMessage.KEY)

    # A lot of checks

    dbaccess = SqliteDbAccess.create_service(main_table=USERS_TABLE)
    user = dbaccess.get(w_filter=("id =" + user_id))
    if user:
        try:
            for key in keys[:-1]:
                s_filter = '' + key + "='" + body[key] + "'"
                dbaccess.update(s_filter=s_filter, w_filter="id =" + user_id, commit=False)

            s_filter = '' + keys[-1] + "='" + body[keys[-1]] + "'"
            dbaccess.update(s_filter=s_filter, w_filter="id =" + user_id)
        except SqliteDbAccess.Error as e:
            if e.type == "INTEGRITY_ERROR":
                return json_error_return(ErrorMessage.EXISTS_ALREADY.format(name=USERS_MESSAGE_NAME))
            return json_error_return(getattr(ErrorMessage, e.type).format(error=e))

        return json_success_return()

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))


@delete('/users/<user_id>')
def delete_user_handler(user_id):
    """Handles user deletion"""

    dbaccess = SqliteDbAccess.create_service(main_table=USERS_TABLE)
    user = dbaccess.get(w_filter=("id =" + user_id))

    if user:
        try:
            w_filter1 = "user =" + user_id
            w_filter2 = "firstFriend =" + user_id + " OR secondFriend =" + user_id
            dbaccess.delete(table="message", w_filter=w_filter1, commit=False)
            dbaccess.delete(table="position", w_filter=w_filter1, commit=False)
            dbaccess.delete(table="conversation_participant", w_filter=w_filter1, commit=False)
            dbaccess.delete(table="friendship", w_filter=w_filter2, commit=False)
            dbaccess.delete(w_filter=w_filter1)
        except SqliteDbAccess.Error as e:
            return json_error_return(getattr(ErrorMessage, e.type).format(error=e))

        return json_success_return()

    return json_error_return(ErrorMessage.DOESNT_EXIST.format(name=USERS_MESSAGE_NAME))
