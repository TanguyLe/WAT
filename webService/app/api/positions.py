from bottle import request, response
from bottle import post, get, delete

from api import apiUtils

#TODO Generalize requests
@post('/users/<user_id>/positions')
def creation_handler(user_id):
	'''Handles user creation'''
	try:
		try:
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		position = data['position']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		c = apiUtils.connectDb()
		c.execute("INSERT INTO position(position, user) VALUES (?, ?)", (position, user_id))
		c.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		c.rollback()
		response.status = "400 Unknown Error"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@get('/users/<user_id>/positions')
def listing_handler(user_id):
	'''Handles user creation'''


	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT id, position, createdDate, user FROM position WHERE position.user = (?)", (user_id,)).fetchone()
	cursor.close()
	
	if(data):
		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn(data)

	#TODO separate case user doesn't exist
	response.status = "400 User doesn't exist nor have a position"
	return

@get('/users/<user_id>/positions/last')
def show_handler(user_id):
	'''Handles user creation'''


	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT id, position, createdDate, user FROM position WHERE position.user = (?) ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
	cursor.close()
	
	if(data):
		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn(data)

	#TODO separate case user doesn't exist
	response.status = "400 User doesn't exist nor have a position"
	return
