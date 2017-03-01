from bottle import request, response
from bottle import post, get, delete, put

from api import apiUtils

@get('/users/<user_id>/conversations')
def listing_handler(user_id):
	'''Handles single user show'''
	# parse input data

	c = apiUtils.connectDb().cursor()

	user = c.execute("SELECT * FROM user WHERE user.id =(?)", (user_id,)).fetchone()
	if(user):
		data = c.execute("SELECT conversation.id, conversation.name FROM conversation, conversation_participant WHERE (conversation_participant.user =(?) AND conversation_participant.conversation = conversation.id)", (user_id)).fetchall()
		c.close()
		return apiUtils.jsonReturn(data)

	c.close()
	response.status = "400 User doesn't exist"
	return

#TODO Generalize requests
@post('/users/<user_id>/conversations')
def creation_handler(user_id):
	'''Handles user creation'''

	try:
		try:
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		name = data['name']
		second_user_id = data['second_user_id']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		c = apiUtils.connectDb()
		c.execute("INSERT INTO conversation(name) VALUES (?)", (name,))
		cursor = c.cursor()
		data = cursor.execute("SELECT id FROM conversation ORDER BY id DESC LIMIT 1").fetchone()

		c.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (data["id"], user_id))
		c.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (data["id"], second_user_id))
		c.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		c.rollback()
		response.status = "400 Unknown Error"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@put('/conversations/<id>')
def update_username_handler(id):
	'''Handles user deletion'''

	try:
		try:
			dataRequest = request.json
		except:
			raise ValueError

		if dataRequest is None:
			raise ValueError

		name = dataRequest["name"]

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT * FROM conversation WHERE conversation.id =(?)", (id,)).fetchone()
	cursor.close()

	if(data):
		try:
			c.execute("UPDATE conversation SET name =? WHERE id =(?)", (name, id))
			c.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			c.rollback()
			
			response.status = "400 Name already taken"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 Conv doesn't exist"
	return

@delete('/conversations/<id>')
def deletion_handler(id):
	'''Handles user deletion'''

	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (id,)).fetchone()
	cursor.close()

	if(data):
		try:
			c.execute("DELETE FROM conversation WHERE (conversation.id =(?))", (id,))
			c.execute("DELETE FROM conversation_participant WHERE (conversation_participant.conversation =(?))", (id,))
			c.execute("DELETE FROM message WHERE (message.conversation =(?))", (id,))
			c.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			c.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 Conversation doesn't exist"
	return
