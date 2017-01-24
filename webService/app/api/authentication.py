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
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		username = data['username']
		password = data['password']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	c = apiUtils.connectDb().cursor()
	data = c.execute("SELECT * FROM user WHERE user.username =(?)", (username,)).fetchone()
	c.close()
	if(data):
		if(data['password'] == password):
			#TODO Of course new things will be necessary there
			return apiUtils.jsonReturn({'loginKey': 'Ok'})
		response.status = "400 Wrong Password"
		return

	response.status = "400 User doesn't exist"
	return
