from bottle import request, response
from bottle import post, get, delete

from api import apiUtils

#TODO Generalize requests
@get('/conversations/<conv_id>/messages')
def listing_handler(conv_id):
	'''Handles user creation'''

	c = apiUtils.connectDb().cursor()
	test = c.execute("SELECT * FROM conversation WHERE (conversation.id =(?))", (conv_id,)).fetchone()
	if(test):
		data = c.execute("""SELECT message.id, message.content, message.createdDate, message.user FROM message WHERE message.conversation =(?)""", (conv_id,)).fetchall()
		c.close()
		return apiUtils.jsonReturn(data)

	c.close()
	response.status = "400 Conversation dosen't exist"
	return
	
	pass

@post('/conversations/<conv_id>/messages')
def creation_handler(conv_id):
	'''Handles user creation'''
	try:
		try:
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		user_id = data['user_id']
		content = data['content']

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		c = apiUtils.connectDb()
		c.execute("INSERT INTO message(content, conversation, user) VALUES (?, ?, ?)", (content, conv_id, user_id))
		c.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		c.rollback()
		response.status = "400 Unknown Error"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@delete('/conversations/<conv_id>/messages/<message_id>')
def deletion_handler(conv_id, message_id):
	'''Handles user creation'''

	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT * FROM message WHERE (message.id =(?) AND message.conversation =(?))", (message_id, conv_id)).fetchone()
	cursor.close()

	if(data):
		try:
			c.execute("DELETE FROM message WHERE (message.id =(?) AND message.conversation =(?))", (message_id, conv_id))
			c.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			c.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	#TODO separate case user doesn't exist
	response.status = "400 Message doesn't exist or is in this conversation"
	return