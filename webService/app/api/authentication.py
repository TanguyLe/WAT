from bottle import request, response
from bottle import post, get

from api import apiUtils

#TODO Generalize requests
@post('/login')
def login_handler():
	'''Handles login'''
	try:

		# parse input data
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		username = body['username']
		password = body['password']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	cursor = apiUtils.getDbConnect().cursor()
	user = cursor.execute("SELECT * FROM user WHERE user.username =(?)", (username,)).fetchone()
	cursor.close()
	if(user):
		if(user['password'] == password):
			#TODO Of course new things will be necessary there
			return apiUtils.jsonReturn({'loginKey': 'Ok'})
		response.status = "400 Wrong Password"
		return

	response.status = "400 User doesn't exist"
	return
