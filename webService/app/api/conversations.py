from bottle import request, response
from bottle import post, get, delete, put

from api.apiUtils.index import jsonSuccessReturn, jsonErrorReturn
from api.apiUtils.index import ErrorMessage, Errors, getDbConnect

@get('/users/<user_id>/conversations')
def listing_handler(user_id):
	'''Handles single user show'''
	# parse input data

	cursor = getDbConnect().cursor()

	user = cursor.execute("SELECT * FROM user WHERE user.id =(?)", (user_id,)).fetchone()
	if(user):
		conversations = cursor.execute("SELECT conversation.id, conversation.name FROM conversation, conversation_participant WHERE (conversation_participant.user =(?) AND conversation_participant.conversation = conversation.id)", (user_id)).fetchall()
		cursor.close()
		return jsonSuccessReturn(conversations)

	cursor.close()
	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="User"))


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
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	try:
		dbConnect = getDbConnect()
		dbConnect.execute("INSERT INTO conversation(name) VALUES (?)", (name,))
		cursor = dbConnect.cursor()
		conversation = cursor.execute("SELECT id FROM conversation ORDER BY id DESC LIMIT 1").fetchone()

		dbConnect.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (conversation["id"], user_id))
		dbConnect.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (conversation["id"], second_user_id))
		dbConnect.commit()
	except Errors as e:
		
		dbConnect.rollback()
		return jsonErrorReturn()

	
	return jsonSuccessReturn()

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
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE conversation.id =(?)", (conv_id,)).fetchone()
	cursor.close()

	if(conversation):
		try:
			dbConnect.execute("UPDATE conversation SET name =? WHERE id =(?)", (convname, conv_id))
			dbConnect.commit()
		except Errors as e:
			
			dbConnect.rollback()
			
			return jsonErrorReturn(ErrorMessage._existsalready.format(name="Conversation name"))

		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="Conversation"))

@delete('/conversations/<conv_id>')
def deletion_handler(conv_id):
	'''Handles user deletion'''

	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (conv_id,)).fetchone()
	cursor.close()

	if(conversation):
		try:
			dbConnect.execute("DELETE FROM conversation_participant WHERE (conversation_participant.conversation =(?))", (conv_id,))
			dbConnect.execute("DELETE FROM message WHERE (message.conversation =(?))", (conv_id,))
			dbConnect.execute("DELETE FROM conversation WHERE (conversation.id =(?))", (conv_id,))
			dbConnect.commit()
		except Errors as e:
			
			dbConnect.rollback()
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="Conversation"))
