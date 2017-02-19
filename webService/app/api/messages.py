from bottle import request, response
from bottle import post, put, get, delete

from api.apiUtils.index import jsonSuccessReturn, jsonErrorReturn
from api.apiUtils.index import ErrorMessage, Errors, getDbConnect


@get('/conversations/<conv_id>/messages')
def listing_handler(conv_id):
	'''Handles user creation'''

	cursor = getDbConnect().cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (conv_id,)).fetchone()
	if(conversation):
		messages = cursor.execute("SELECT message.id, message.content, message.createdDate, message.user FROM message WHERE message.conversation =(?)", (conv_id,)).fetchall()
		cursor.close()
		return jsonSuccessReturn(messages)

	cursor.close()
	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="Conversation"))
	
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
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	try:
		dbConnect = getDbConnect()
		dbConnect.execute("INSERT INTO message(content, conversation, user) VALUES (?, ?, ?)", (content, conv_id, user_id))
		dbConnect.commit()
	except Errors as e:
		
		dbConnect.rollback()
		return jsonErrorReturn()

	
	return jsonSuccessReturn()

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
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	message = cursor.execute("SELECT * FROM message WHERE (message.id =(?))", (msg_id, )).fetchone()
	cursor.close()

	if(message):
		try:
			dbConnect.execute("UPDATE message SET content =? WHERE id =(?)", (content, msg_id))
			dbConnect.commit()
		except Errors as e:
			
			dbConnect.rollback()
			
			return jsonErrorReturn()

		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="Message"))

@delete('/messages/<msg_id>')
def deletion_handler(msg_id):
	'''Handles user creation'''

	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	message = cursor.execute("SELECT * FROM message WHERE (message.id =(?))", (msg_id, )).fetchone()
	cursor.close()

	if(message):
		try:
			dbConnect.execute("DELETE FROM message WHERE (message.id =(?))", (msg_id,))
			dbConnect.commit()
		except Errors as e:
			
			dbConnect.rollback()
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	#TODO separate case user doesn't exist
	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="Message"))
