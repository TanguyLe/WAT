from bottle import request, response
from bottle import post, get, delete

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
@post('/conversations')
def creation_handler():
	'''Handles user creation'''

	try:
		try:
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		name = data['name']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		c = apiUtils.connectDb()
		c.execute("INSERT INTO conversation(name) VALUES (?)", (name,))
		c.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		c.rollback()
		response.status = "400 Unknown Error"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

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