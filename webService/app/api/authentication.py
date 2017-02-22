from bottle import request, response
from bottle import post, get

from api.utils.index import jsonSuccessReturn, jsonErrorReturn
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, usersTable, usersMessageName


@post('/login')
def login_handler():
	'''Handles login'''
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

	dbaccess = sqliteDbAccess.create_service()
	user = dbaccess.get(table=usersTable, wfilter=("username =" + username))
	if(user):
		if(user['password'] == password):
			#TODO Of course new things will be necessary there
			return jsonSuccessReturn({'loginKey': 'Ok'})
		return jsonErrorReturn(ErrorMessage._password)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=usersMessageName))
