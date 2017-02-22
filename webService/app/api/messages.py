from bottle import request, response
from bottle import post, put, get, delete

from api.utils.index import jsonSuccessReturn, jsonErrorReturn
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, conversationsMessageName, messagesMessageName
from api.constants.index import conversationsTable, messagesTable


@get('/conversations/<conv_id>/messages')
def listing_handler(conv_id):
	'''Handles listing of conv messages'''

	dbaccess = sqliteDbAccess.create_service()
	conversation = dbaccess.get(table=conversationsTable, wfilter=("id =" + conv_id))
	if(conversation):
		messages = dbaccess.get(table=messagesTable, wfilter=("conversation =" + conv_id))
		return jsonSuccessReturn(messages)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=conversationsMessageName))

@post('/conversations/<conv_id>/messages')
def creation_handler(conv_id):
	'''Handles message creation'''
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
		dbaccess = sqliteDbAccess.create_service()
		dbaccess.insert(table=messagesTable, 
						dict={"content": content, "conversation" : conv_id, "user": user_id})
	except sqliteDbAccess.Errors as e:
		return jsonErrorReturn()

	return jsonSuccessReturn()

@put('/messages/<msg_id>')
def update_username_handler(msg_id):
	'''Handles message content update'''

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

	dbaccess = sqliteDbAccess.create_service(mainTable=messagesTable)
	message = dbaccess.get(wfilter=("id =" + msg_id))

	if(message):
		try:
			dbaccess.update(sfilter=('content ="' + content + '"'), wfilter=("id =" + msg_id))
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn()

		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=messageMessage))

@delete('/messages/<msg_id>')
def deletion_handler(msg_id):
	'''Handles message deletion'''

	dbaccess = sqliteDbAccess.create_service(mainTable=messagesTable)
	message = dbaccess.get(wfilter=("id =" + msg_id))

	if(message):
		try:
			dbaccess.delete(wfilter="id =" + msg_id)
		except sqliteDbAccess.Errors as e:
			
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	#TODO separate case user doesn't exist
	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=messageMessage))
