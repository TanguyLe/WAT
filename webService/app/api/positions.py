from bottle import request, response
from bottle import post, get, delete

from api.apiUtils.index import jsonSuccessReturn, jsonErrorReturn
from api.apiUtils.index import ErrorMessage, Errors, getDbConnect


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
		dbConnect = getDbConnect()
		dbConnect.execute("INSERT INTO position(position, user) VALUES (?, ?)", (position, user_id))
		dbConnect.commit()
	except Errors as e:
		
		dbConnect.rollback()
		return jsonErrorReturn()

	
	return jsonSuccessReturn()

@get('/users/<user_id>/positions')
def listing_handler(user_id):
	'''Handles user creation'''


	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	positions = cursor.execute("SELECT id, position, createdDate, user FROM position WHERE position.user = (?)", (user_id,)).fetchone()
	cursor.close()
	
	if(positions):
		
		return jsonSuccessReturn(positions)

	#TODO separate case user doesn't exist
	return jsonErrorReturn("User doesn't exist or doesn't have a position recorded")

@get('/users/<user_id>/positions/last')
def show_handler(user_id):
	'''Handles user creation'''


	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	position = cursor.execute("SELECT id, position, createdDate, user FROM position WHERE position.user = (?) ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
	cursor.close()
	
	if(position):
		
		return jsonSuccessReturn(position)

	#TODO separate case user doesn't exist
	return jsonErrorReturn(ErrorMessage._nouserorposition)
