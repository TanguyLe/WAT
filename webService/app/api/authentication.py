from bottle import request, response
from bottle import post, get, put, delete

import re, json

_usersObjectsList = []                # the set of names

@get('/users')
def listing_handler():
	'''Handles users listing'''

	response.headers['Content-Type'] = 'application/json'
	response.headers['Cache-Control'] = 'no-cache'
	_usernamesList = []

	for user in _usersObjectsList:
		_usernamesList.append(user['username'])
	return json.dumps({'users': list(_usernamesList)})
	pass

@get('/users/<username>')
def showing_handler(username):
	'''Handles user show'''
	# parse input data

	try:
		user = next(x for x in _usersObjectsList if x['username'] == username)			
	except StopIteration:
		# if bad request data, return 400 Bad Request
		response.status = "400 User doesn't exist"
		return

	newUser = dict(user)
	del newUser['password']

	# return 200 Success
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(newUser)


@post('/login')
def login_handler():
	'''Handle login'''
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

		_usernamesList = []
		for user in _usersObjectsList:
			_usernamesList.append(user['username'])

		if not(username in _usernamesList):
			response.status = "400 User doesn't exist"
			return

	except ValueError:
		# if bad request data, return 400 Bad Request
		response.status = "400 Value Error"
		return

	try:
		user = next(x for x in _usersObjectsList if x['username'] == username)			
	except StopIteration:
		# if bad request data, return 400 Bad Request
		response.status = "400 User doesn't exist"
		return

	if(user['password'] == password):
		# return 200 Success
		response.headers['Content-Type'] = 'application/json'
		return json.dumps({'loginKey': 'Ok'})
	else:
		response.status = "400 Wrong Password"
		return



@post('/users')
def creation_handler():
	'''Handles user creation'''

	try:
		print(request.json)
		# parse input data
		try:
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		username = data['username']
		password = data['password']

		_usernamesList = []
		for user in _usersObjectsList:
			_usernamesList.append(user['username'])

		if username in _usernamesList:
			raise KeyError

	except ValueError:
		# if bad request data, return 400 Bad Request
		response.status = "400 Value Error"
		return

	except KeyError:
		# if name already exists, return 409 Conflict
		response.status = "409 Value Conflict: Username taken"
		return

	# add user
	_usersObjectsList.append({'username': username, 'password': password})

	# return 200 Success
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({'username': username})
