from bottle import request, response
from bottle import post, get, delete, route

from api import apiUtils

#TODO Generalize requests
@get('/users')
def listing_handler():
	'''Handles users listing'''

	_users = []
	c = apiUtils.connectDb().cursor()
	c.execute("""SELECT id, username, password FROM user""")
	data = c.fetchall()
	c.close()
	return apiUtils.jsonReturn(data)

	pass

@get('/users/<id>')
def show_handler(id):
	'''Handles single user show'''
	# parse input data

	c = apiUtils.connectDb().cursor()
	data = c.execute("SELECT * FROM user WHERE user.id =(?)", (id,)).fetchone()
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
		c.execute("INSERT INTO user(username, password) VALUES (?,?)", (username, password))
		c.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		c.rollback()
		response.status = "400 User exists already"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@route('/users/<id>', 'PATCH')
def update_username_handler(id):
	'''Handles user deletion'''

	try:
		try:
			dataRequest = request.json
		except:
			raise ValueError

		if dataRequest is None:
			raise ValueError

		username = dataRequest['username']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return


	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT * FROM user WHERE user.id =(?)", (id,)).fetchone()
	cursor.close()

	if(data):
		try:
			c.execute("UPDATE user SET username =? WHERE id =(?)", (username, id))
			c.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			c.rollback()
			
			response.status = "400 Name already taken"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 User doesn't exist"
	return


@delete('/users/<id>')
def deletion_handler(id):
	'''Handles user deletion'''

	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT * FROM user WHERE user.id =(?)", (id,)).fetchone()
	cursor.close()

	if(data):
		try:
			c.execute("DELETE FROM message WHERE message.user=(?)", (id,))
			c.execute("DELETE FROM conversation_participant WHERE conversation_participant.user=(?)", (id,))
			c.execute("DELETE FROM friendship WHERE friendship.firstFriend=(?) OR friendship.secondFriend=(?)", (id, id))
			c.execute("DELETE FROM user WHERE user.id =(?)", (id,))
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
