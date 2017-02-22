from bottle import request, response
from bottle import post, get, delete

from api.utils.index import jsonSuccessReturn, jsonErrorReturn
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, conversationsMessageName
from api.constants.index import conversationsTable, conversationParticipantsTable


@get('/conversations/<conv_id>/participants')
def listing_handler(conv_id):
	'''Handles the listing of participants in a conv'''

	dbaccess = sqliteDbAccess.create_service()
	conversation = dbaccess.get(table=conversationsTable, wfilter=("id =" + conv_id))

	if(conversation):

		params = {
					"user": 
						{
							"attributes": ["id", "username"], 
						 	"join": "id"
					 	}, 
				    "conversation_participant": 
				    	{
				    		"attributes": [], 
				    		"join": "user"
			    		}
		    	 }
		wfilter = "conversation_participant.conversation =" + conv_id

		participants = dbaccess.getjoin(params=params, wfilter=wfilter)

		return jsonSuccessReturn(participants)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=conversationsMessageName))
	
	pass

@post('/conversations/<conv_id>/participants')
def creation_handler(conv_id):
	'''Handles conversation creation'''
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
		dbaccess = sqliteDbAccess.create_service()
		dbaccess.insert(table=conversationParticipantsTable, 
						dict={"conversation": conv_id, "user": user_id})
	except sqliteDbAccess.Errors as e:
		return jsonErrorReturn(ErrorMessage._userinconv)

	return jsonSuccessReturn()

@delete('/conversations/<conv_id>/participants/<user_id>')
def deletion_handler(conv_id, user_id):
	'''Handles conversation deletion'''


	dbaccess = sqliteDbAccess.create_service(mainTable=conversationParticipantsTable)
	participants = dbaccess.get(wfilter=("conversation =" + conv_id + " AND user =" + user_id))
	if(participants):
		try:
			dbaccess.delete(wfilter=("conversation =" + conv_id + " AND user =" + user_id))
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn()
		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._usernotinconv)
