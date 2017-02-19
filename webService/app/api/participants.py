from bottle import request, response
from bottle import post, get, delete

from api.apiUtils.index import jsonSuccessReturn, jsonErrorReturn
from api.apiUtils.index import ErrorMessage, Errors, getDbConnect


@get('/conversations/<conv_id>/participants')
def listing_handler(conv_id):
	'''Handles user creation'''

	cursor = getDbConnect().cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (conv_id,)).fetchone()
	if(conversation):
		participants = cursor.execute("SELECT user.id, user.username FROM user, conversation_participant WHERE (user.id = conversation_participant.user AND conversation_participant.conversation =(?))", (conv_id,)).fetchall()
		cursor.close()
		return jsonSuccessReturn(participants)

	cursor.close()
	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="Conversation"))
	
	pass

@post('/conversations/<conv_id>/participants')
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

	except ValueError:
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	try:
		dbConnect = getDbConnect()
		dbConnect.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (conv_id, user_id))
		dbConnect.commit()
	except Errors as e:
		
		dbConnect.rollback()
		return jsonErrorReturn(ErrorMessage._userinconv)

	
	return jsonSuccessReturn()

@delete('/conversations/<conv_id>/participants/<user_id>')
def deletion_handler(conv_id, user_id):
	'''Handles user creation'''

	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	participants = cursor.execute("SELECT * FROM conversation_participant WHERE (conversation_participant.conversation =(?) AND conversation_participant.user =(?))", (conv_id, user_id)).fetchone()
	cursor.close()

	if(participants):
		try:
			dbConnect.execute("DELETE FROM conversation_participant WHERE (conversation_participant.conversation =(?) AND conversation_participant.user =(?))", (conv_id, user_id))
			dbConnect.commit()
		except Errors as e:
			
			dbConnect.rollback()
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._usernotinconv)
