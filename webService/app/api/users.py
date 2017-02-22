from bottle import request, response
from bottle import post, get, delete, route

from api.utils.index import jsonSuccessReturn, jsonErrorReturn
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, usersTable, usersMessageName


@get('/users')
def listing_handler():
	'''Handles users listing'''

	dbaccess = sqliteDbAccess.create_service()
	users = dbaccess.get(table=usersTable)

	return jsonSuccessReturn(users)

@get('/users/<user_id>')
def show_handler(user_id):
	'''Handles single user show'''

	dbaccess = sqliteDbAccess.create_service()
	user = dbaccess.get(table=usersTable, wfilter=("id =" + user_id), multiple=False)

	if(user):
		return jsonSuccessReturn(user)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=userMessage))


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
		user = dbaccess.insert(table=usersTable, dict={"username": username, "password": password})
	except sqliteDbAccess.Errors as e:
		return jsonErrorReturn(ErrorMessage._existsalready.format(name=userMessage))
	
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

	dbaccess = sqliteDbAccess.create_service(mainTable=usersTable)
	user = dbaccess.get(wfilter=("id =" + user_id))
	if(user):
		try:
			for key in keys[:-1]:
				sfilter = '' + key + '="' + body[key] + '"'
				dbaccess.update(sfilter=sfilter, wfilter="id =" + user_id, commit=False)
				
			sfilter = '' + keys[-1] + '="' + body[keys[-1]] + '"'
			dbaccess.update(sfilter=sfilter, wfilter="id =" + user_id)
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn(ErrorMessage._existsalready.format(name=userMessage))
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=userMessage))


@delete('/users/<user_id>')
def deletion_handler(user_id):
	'''Handles user deletion'''

	dbaccess = sqliteDbAccess.create_service(mainTable=usersTable)
	user = dbaccess.get(wfilter=("id =" + user_id))

	if(user):
		try:
			wfilter1 = "user =" + user_id
			wfilter2 = "firstFriend =" + user_id + " OR secondFriend =" + user_id
			dbaccess.delete(table="message", wfilter=wfilter1, commit=False)
			dbaccess.delete(table="position", wfilter=wfilter1, commit=False)
			dbaccess.delete(table="conversation_participant", wfilter=wfilter, commit=False)
			dbaccess.delete(table="friendship", wfilter=wfilter2, commit=False)
			dbaccess.delete(wfilter=wfilter1)
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=userMessage))
