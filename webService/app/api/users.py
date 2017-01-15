from bottle import request, response
from bottle import post, get, delete

from api import apiUtils

#TODO Generalize requests
@get('/users')
def listing_handler():
	'''Handles users listing'''

	_users = []
	c = apiUtils.connectDb().cursor()
	c.execute("""SELECT username, password FROM users""")
	data = c.fetchall()
	c.close()
	return apiUtils.jsonReturn(data)

	pass

@get('/users/<username>')
def show_handler(username):
	'''Handles single user show'''
	# parse input data

	c = apiUtils.connectDb().cursor()
	data = c.execute("SELECT * FROM users WHERE users.username =(?)", (username,)).fetchone()
	c.close()
	if(data):
		return apiUtils.jsonReturn(data)

	response.status = "400 User doesn't exist"
	return


@post('/users')
def creation_handler():
	'''Handles user creation'''

	try:
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

	try:
		c = apiUtils.connectDb()
		c.execute("INSERT INTO users VALUES (?,?)", (username, password))
		c.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		c.rollback()
		response.status = "400 User exists already"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@delete('/users/<username>')
def deletion_handler(username):
	'''Handles user deletion'''

	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT * FROM users WHERE users.username =(?)", (username,)).fetchone()
	cursor.close()

	if(data):
		try:
			c.execute("DELETE FROM users WHERE users.username =(?)", (username,))
			c.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			c.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 User doesn't exist"
	return
