from bottle import request, response
from bottle import post, get, delete, route

from api.apiUtils.index import jsonSuccessReturn, jsonErrorReturn
from api.apiUtils.index import ErrorMessage, sqliteDbAccess


@get('/users')
def listing_handler():
	'''Handles users listing'''

	dbaccess = sqliteDbAccess.create_service()
	users = dbaccess.get(table="user")

	return jsonSuccessReturn(users)

@get('/users/<user_id>')
def show_handler(user_id):
	'''Handles single user show'''

	dbaccess = sqliteDbAccess.create_service()
	user = dbaccess.get(table="user", wfilter=("user.id =" + user_id))

	if(user):
		return jsonSuccessReturn(user)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="User"))


@post('/users')
def creation_handler():
	'''Handles user creation'''

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
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	try:
		dbaccess = sqliteDbAccess.create_service()
		user = dbaccess.insert(table="user", dict={"username": username, "password": password})
	except sqliteDbAccess.Errors as e:
		return jsonErrorReturn(ErrorMessage._existsalready.format(name="User"))
	
	return jsonSuccessReturn()

@route('/users/<user_id>', 'PATCH')
def update_username_handler(user_id):
	'''Handles user deletion'''

	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		keys = list(body.keys())

	except ValueError:
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)
	
	### A lot of checks

	dbaccess = sqliteDbAccess.create_service()
	user = dbaccess.get(table="user", wfilter=("user.id =" + user_id))

	print(keys)
	if(user):
		try:
			for key in keys[:-1]:
				sfilter = '' + key + '="' + body[key] + '"'
				dbaccess.update(table="user", sfilter=sfilter, wfilter="id=" + user_id, commit=False)
				
			sfilter = '' + keys[-1] + '="' + body[keys[-1]] + '"'
			dbaccess.update(table="user", sfilter=sfilter, wfilter="id=" + user_id)
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn(ErrorMessage._existsalready.format(name="User"))
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="User"))


@delete('/users/<user_id>')
def deletion_handler(user_id):
	'''Handles user deletion'''

	dbaccess = sqliteDbAccess.create_service()
	user = dbaccess.get(table="user", wfilter=("user.id =" + user_id))

	if(user):
		try:
			dbaccess.delete(table="message", wfilter=("message.user=" + user_id), commit=False)
			dbaccess.delete(table="position", wfilter=("position.user=" + user_id), commit=False)
			dbaccess.delete(table="conversation_participant", wfilter=("conversation_participant.user=" + user_id), commit=False)
			dbaccess.delete(table="friendship", wfilter=("friendship.firstFriend=" + user_id + " OR friendship.secondFriend=" + user_id), commit=False)
			dbaccess.delete(table="user", wfilter=("user.id=" + user_id))
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="User"))
