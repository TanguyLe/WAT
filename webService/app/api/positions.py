from bottle import request, response
from bottle import post, get, delete

from api import apiUtils

#TODO Generalize requests
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
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		dbConnect = apiUtils.getDbConnect()
		dbConnect.execute("INSERT INTO position(position, user) VALUES (?, ?)", (position, user_id))
		dbConnect.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		dbConnect.rollback()
		response.status = "400 Unknown Error"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@get('/users/<user_id>/positions')
def listing_handler(user_id):
	'''Handles user creation'''


	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	positions = cursor.execute("SELECT id, position, createdDate, user FROM position WHERE position.user = (?)", (user_id,)).fetchone()
	cursor.close()
	
	if(positions):
		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn(positions)

	#TODO separate case user doesn't exist
	response.status = "400 User doesn't exist nor have a position"
	return

@get('/users/<user_id>/positions/last')
def show_handler(user_id):
	'''Handles user creation'''


	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	position = cursor.execute("SELECT id, position, createdDate, user FROM position WHERE position.user = (?) ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
	cursor.close()
	
	if(position):
		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn(position)

	#TODO separate case user doesn't exist
	response.status = "400 User doesn't exist nor have a position"
	return
