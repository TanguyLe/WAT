from bottle import request, response
from bottle import post, put, get, delete

from api import apiUtils

#TODO Generalize requests
@get('/conversations/<conv_id>/messages')
def listing_handler(conv_id):
	'''Handles user creation'''

	cursor = apiUtils.getDbConnect().cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (conv_id,)).fetchone()
	if(conversation):
		messages = cursor.execute("SELECT message.id, message.content, message.createdDate, message.user FROM message WHERE message.conversation =(?)", (conv_id,)).fetchall()
		cursor.close()
		return apiUtils.jsonReturn(messages)

	cursor.close()
	response.status = "400 Conversation dosen't exist"
	return
	
	pass

@post('/conversations/<conv_id>/messages')
def creation_handler(conv_id):
	'''Handles user creation'''
	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		user_id = body['user_id']
		content = body['content']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		dbConnect = apiUtils.getDbConnect()
		dbConnect.execute("INSERT INTO message(content, conversation, user) VALUES (?, ?, ?)", (content, conv_id, user_id))
		dbConnect.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		dbConnect.rollback()
		response.status = "400 Unknown Error"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@put('/messages/<msg_id>')
def update_username_handler(msg_id):
	'''Handles user deletion'''

	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		content = body["content"]

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	message = cursor.execute("SELECT * FROM message WHERE (message.id =(?))", (msg_id, )).fetchone()
	cursor.close()

	if(message):
		try:
			dbConnect.execute("UPDATE message SET content =? WHERE id =(?)", (content, msg_id))
			dbConnect.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			dbConnect.rollback()
			
			response.status = "400 Name already taken"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 Message doesn't exist"
	return

@delete('/messages/<msg_id>')
def deletion_handler(msg_id):
	'''Handles user creation'''

	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	message = cursor.execute("SELECT * FROM message WHERE (message.id =(?))", (msg_id, )).fetchone()
	cursor.close()

	if(message):
		try:
			dbConnect.execute("DELETE FROM message WHERE (message.id =(?))", (msg_id,))
			dbConnect.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			dbConnect.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	#TODO separate case user doesn't exist
	response.status = "400 Message doesn't exist"
	return
