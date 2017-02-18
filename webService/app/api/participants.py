from bottle import request, response
from bottle import post, get, delete

from api import apiUtils

#TODO Generalize requests
@get('/conversations/<conv_id>/participants')
def listing_handler(conv_id):
	'''Handles user creation'''

	cursor = apiUtils.getDbConnect().cursor()
	conversation = cursor.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (conv_id,)).fetchone()
	if(conversation):
		participants = cursor.execute("SELECT user.id, user.username FROM user, conversation_participant WHERE (user.id = conversation_participant.user AND conversation_participant.conversation =(?))", (conv_id,)).fetchall()
		cursor.close()
		return apiUtils.jsonReturn(participants)

	cursor.close()
	response.status = "400 Conversation dosen't exist"
	return
	
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
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		dbConnect = apiUtils.getDbConnect()
		dbConnect.execute("INSERT INTO conversation_participant(conversation, user) VALUES (?, ?)", (conv_id, user_id))
		dbConnect.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		dbConnect.rollback()
		response.status = "400 User already in conversation"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@delete('/conversations/<conv_id>/participants/<user_id>')
def deletion_handler(conv_id, user_id):
	'''Handles user creation'''

	dbConnect = apiUtils.getDbConnect()
	cursor = dbConnect.cursor()
	participants = cursor.execute("SELECT * FROM conversation_participant WHERE (conversation_participant.conversation =(?) AND conversation_participant.user =(?))", (conv_id, user_id)).fetchone()
	cursor.close()

	if(participants):
		try:
			dbConnect.execute("DELETE FROM conversation_participant WHERE (conversation_participant.conversation =(?) AND conversation_participant.user =(?))", (conv_id, user_id))
			dbConnect.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			dbConnect.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 User doesn't participate in this conversation"
	return
