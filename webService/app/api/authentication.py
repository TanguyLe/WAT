from bottle import request, response
from bottle import post, get

from api.apiUtils.index import jsonSuccessReturn, jsonErrorReturn
from api.apiUtils.index import ErrorMessage, Errors, getDbConnect


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
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	cursor = getDbConnect().cursor()
	user = cursor.execute("SELECT * FROM user WHERE user.username =(?)", (username,)).fetchone()
	cursor.close()
	if(user):
		if(user['password'] == password):
			#TODO Of course new things will be necessary there
			return jsonSuccessReturn({'loginKey': 'Ok'})
		return jsonErrorReturn(ErrorMessage._password)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="User"))
