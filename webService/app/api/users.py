from bottle import request, response
from bottle import post, get, delete, route

from api import apiUtils

#TODO Generalize requests
@get('/users')
def listing_handler():
	'''Handles users listing'''

	cursor = apiUtils.getDbConnect().cursor()
	cursor.execute("SELECT * FROM user")
	users = cursor.fetchall()
	cursor.close()
	return apiUtils.jsonReturn(users)

	pass

@get('/users/<user_id>')
def show_handler(user_id):
	'''Handles single user show'''
	# parse input data

	dbConnect = apiUtils.getDbConnect().cursor()
	user = dbConnect.execute("SELECT * FROM user WHERE user.id =(?)", (user_id,)).fetchone()
	dbConnect.close()
	if(user):
		return apiUtils.jsonReturn(users)

	response.status = "400 User doesn't exist"
	return


@post('/users')
def creation_handler():
	'''Handles user creation'''

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
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		dbConnect = apiUtils.getDbConnect()
		dbConnect.execute("INSERT INTO user(username, password) VALUES (?,?)", (username, password))
		dbConnect.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		dbConnect.rollback()
		response.status = "400 User exists already"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@route('/users/<user_id>', 'PATCH')
def update_username_handler(user_id):
	'''Handles user deletion'''

	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		keys = body.keys()

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return
	
	### A lot of checks

	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	user = cursor.execute("SELECT * FROM user WHERE user.id =(?)", (user_id,)).fetchone()
	cursor.close()

	if(user):
		try:
			for key in keys:
				dbConnect.execute("UPDATE user SET " + key + " =? WHERE id =(?)", (dataRequest[key], user_id))
			dbConnect.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			dbConnect.rollback()
			
			response.status = "400 Name already taken"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 User doesn't exist"
	return


@delete('/users/<user_id>')
def deletion_handler(user_id):
	'''Handles user deletion'''

	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	user = cursor.execute("SELECT * FROM user WHERE user.id =(?)", (user_id,)).fetchone()
	cursor.close()

	if(user):
		try:
			dbConnect.execute("DELETE FROM message WHERE message.user=(?)", (user_id,))
			dbConnect.execute("DELETE FROM position WHERE position.user=(?)", (user_id,))
			dbConnect.execute("DELETE FROM conversation_participant WHERE conversation_participant.user=(?)", (user_id,))
			dbConnect.execute("DELETE FROM friendship WHERE friendship.firstFriend=(?) OR friendship.secondFriend=(?)", (user_id, user_id))
			dbConnect.execute("DELETE FROM user WHERE user.id =(?)", (user_id,))
			dbConnect.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			c.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 User doesn't exist"
	return
