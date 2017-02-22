from bottle import request, response
from bottle import post, get, delete, put

from api.utils.index import jsonSuccessReturn, jsonErrorReturn
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, usersMessageName, conversationsMessageName, messagesTable
from api.constants.index import usersTable, conversationParticipantsTable, conversationsTable


@get('/users/<user_id>/conversations')
def listing_handler(user_id):
	'''Handles listing of the conversations of a user'''
	
	dbaccess = sqliteDbAccess.create_service()
	user = dbaccess.get(table=usersTable, wfilter=("id =" + user_id))

	if(user):
		params = {
					"conversation": 
						{
							"attributes": ["id", "name"], 
						 	"join": "id"
					 	}, 
				    "conversation_participant": 
				    	{
				    		"attributes": [], 
				    		"join": "conversation"
			    		}
		    	 }
		wfilter = "conversation_participant.user =" + user_id

		conversations = dbaccess.getjoin(params=params, wfilter=wfilter)
			
		return jsonSuccessReturn(conversations)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=usersMessageName))


@post('/users/<user_id>/conversations')
def creation_handler(user_id):
	'''Handles conversation creation'''

	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		convname = body['convname']
		second_user_id = body['user_id']

	except ValueError:
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	try:
		dbaccess = sqliteDbAccess.create_service(mainTable=conversationParticipantsTable)
		dbaccess.insert(table=conversationsTable, dict={"name": convname})

		conversation = dbaccess.getlast(table=conversationsTable)

		dbaccess.insert(dict={"conversation": conversation["id"], "user": user_id})
		dbaccess.insert(dict={"conversation": conversation["id"], "user": second_user_id})
	except sqliteDbAccess.Errors as e:
		return jsonErrorReturn()

	return jsonSuccessReturn()

@put('/conversations/<conv_id>')
def update_username_handler(conv_id):
	'''Handles conversation name change'''

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

	dbaccess = sqliteDbAccess.create_service(mainTable=conversationsTable)
	conversation = dbaccess.get(wfilter=("id = " + conv_id))

	if(conversation):
		try:
			dbaccess.update(sfilter=("name = '" + convname + "'"), wfilter=("id = " + conv_id))
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn(ErrorMessage._existsalready.format(name=conversationsMessageName))

		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=conversationsMessageName))

@delete('/conversations/<conv_id>')
def deletion_handler(conv_id):
	'''Handles conversation deletion'''

	dbaccess = sqliteDbAccess.create_service(mainTable=conversationsTable)
	conversation = dbaccess.get(wfilter=("id = " + conv_id))

	if(conversation):
		try:
			wfilter = "conversation =" + conv_id
			dbaccess.delete(table=conversationParticipantsTable, wfilter=wfilter, commit=False)
			dbaccess.delete(table=messagesTable, wfilter=wfilter, commit=False)
			dbaccess.delete(wfilter=("id =" + conv_id))
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=conversationsMessageName))
