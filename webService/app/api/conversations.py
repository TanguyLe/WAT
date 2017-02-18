from bottle import request, response
from bottle import post, get, delete, put

from api import apiUtils

@get('/users/<user_id>/conversations')
def listing_handler(user_id):
	'''Handles single user show'''
	# parse input data

	cursor = apiUtils.getDbConnect().cursor()

	user = cursor.execute("SELECT * FROM user WHERE user.id =(?)", (user_id,)).fetchone()
	if(user):
		user = cursor.execute("SELECT conversation.id, conversation.name FROM conversation, conversation_participant WHERE (conversation_participant.user =(?) AND conversation_participant.conversation = conversation.id)", (user_id)).fetchall()
		cursor.close()
		return apiUtils.jsonReturn(user)

	cursor.close()
	response.status = "400 User doesn't exist"
	return

#TODO Generalize requests
@post('/users/<user_id>/conversations')
def creation_handler(user_id):
	'''Handles user creation'''

	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		convname = body['convname']
		second_user_id = body['second_user_id']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		dbConnect = apiUtils.getDbConnect()
		dbConnect.execute("INSERT INTO conversation(name) VALUES (?)", (name,))
		cursor = dbConnect.cursor()
		conversation = cursor.execute("SELECT id FROM conversation ORDER BY id DESC LIMIT 1").fetchone()

		dbConnect.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (conversation["id"], user_id))
		dbConnect.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (conversation["id"], second_user_id))
		dbConnect.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		dbConnect.rollback()
		response.status = "400 Unknown Error"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@put('/conversations/<conv_id>')
def update_username_handler(conv_id):
	'''Handles user deletion'''

	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		convname = body["convname"]

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE conversation.id =(?)", (conv_id,)).fetchone()
	cursor.close()

	if(conversation):
		try:
			dbConnect.execute("UPDATE conversation SET name =? WHERE id =(?)", (convname, conv_id))
			dbConnect.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			dbConnect.rollback()
			
			response.status = "400 Name already taken"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 Conv doesn't exist"
	return

@delete('/conversations/<conv_id>')
def deletion_handler(conv_id):
	'''Handles user deletion'''

	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (conv_id,)).fetchone()
	cursor.close()

	if(conversation):
		try:
			dbConnect.execute("DELETE FROM conversation_participant WHERE (conversation_participant.conversation =(?))", (conv_id,))
			dbConnect.execute("DELETE FROM message WHERE (message.conversation =(?))", (conv_id,))
			dbConnect.execute("DELETE FROM conversation WHERE (conversation.id =(?))", (conv_id,))
			dbConnect.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			dbConnect.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 Conversation doesn't exist"
	return
