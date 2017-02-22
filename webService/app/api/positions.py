from bottle import request, response
from bottle import post, get, delete

from api.utils.index import jsonSuccessReturn, jsonErrorReturn
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, positionsTable


@post('/users/<user_id>/positions')
def creation_handler(user_id):
	'''Handles user creation'''
	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		position = body['position']

	except ValueError:
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	try:
		dbaccess = sqliteDbAccess.create_service()
		user = dbaccess.insert(table=positionsTable, dict={"position": position, "user": user_id})
	except sqliteDbAccess.Errors as e:
		return jsonErrorReturn()

	
	return jsonSuccessReturn()

@get('/users/<user_id>/positions')
def listing_handler(user_id):
	'''Handles user creation'''

	dbaccess = sqliteDbAccess.create_service()
	positions = dbaccess.get(table=positionsTable, wfilter=("user =" + user_id))

	if(positions):
		return jsonSuccessReturn(positions)

	#TODO separate case user doesn't exist
	return jsonErrorReturn(ErrorMessage._nouserorposition)

@get('/users/<user_id>/positions/last')
def show_handler(user_id):
	'''Handles user creation'''

	dbaccess = sqliteDbAccess.create_service()
	wfilter = "user =" + user_id + " ORDER BY id DESC LIMIT 1" 
	position = dbaccess.get(table=positionsTable, wfilter=wfilter, multiple=False)

	if(position):
		return jsonSuccessReturn(position)

	#TODO separate case user doesn't exist
	return jsonErrorReturn(ErrorMessage._nouserorposition)
