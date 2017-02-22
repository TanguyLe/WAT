from bottle import request, response
from bottle import post, get, delete

from api.utils.index import jsonSuccessReturn, jsonErrorReturn
from api.utils.index import sqliteDbAccess

from api.constants.index import ErrorMessage, usersMessageName, friendshipsMessageName
from api.constants.index import usersTable, friendshipsTable


@get('/users/<user_id>/friends')
def listing_handler(user_id):
	'''Handles the listing of a user's friends'''

	dbaccess = sqliteDbAccess.create_service()
	user = dbaccess.get(table=usersTable, wfilter=("id =" + user_id))
	if(user):
		params = {
					"user": 
						{
							"attributes": ["id", "username"], 
						 	"join": "id"
					 	}, 
				    "friendship": 
				    	{
				    		"attributes": [], 
				    		"join": "firstFriend"
			    		}
		    	 }
		wfilter = "friendship.secondFriend =" + user_id

		users = dbaccess.getjoin(params=params, wfilter=wfilter)

		return jsonSuccessReturn(users)

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=usersMessageName))

@post('/users/<user_id>/friends')
def creation_handler(user_id):
	'''Handles friendship creation'''

	try:
		try:
			body = request.json
		except:
			raise ValueError

		if body is None:
			raise ValueError

		friend_id = body['user_id']

	except ValueError:
		return jsonErrorReturn(ErrorMessage._value)

	except KeyError:
		return jsonErrorReturn(ErrorMessage._key)

	try:
		dbaccess = sqliteDbAccess.create_service()
		wfilter = "firstFriend =" + str(friend_id) + " AND secondFriend =" + str(user_id)
		friendship = dbaccess.get(table=friendshipsTable, wfilter=wfilter)
		if(friendship):
			return jsonErrorReturn(ErrorMessage._existsalready.format(name=friendshipsMessageName))

		dbaccess.insert(table=friendshipsTable, dict={"firstFriend": user_id, "secondFriend": friend_id})
		dbaccess.insert(table=friendshipsTable, dict={"firstFriend": friend_id, "secondFriend": user_id})
	except sqliteDbAccess.Errors as e:
		return jsonErrorReturn()

	return jsonSuccessReturn()


@delete('/users/<user_id>/friends/<friend_id>')
def deletion_handler(user_id, friend_id):
	'''Handles friendship deletion'''

	dbaccess = sqliteDbAccess.create_service(mainTable=friendshipsTable)
	wfilter1 = "firstFriend =" + friend_id + " AND secondFriend =" + user_id
	wfilter2 = "firstFriend =" + user_id + " AND secondFriend =" + friend_id
	friendship = dbaccess.get(wfilter=wfilter1)

	if(friendship):
		try:
			dbaccess.delete(wfilter=wfilter1)
			dbaccess.delete(wfilter=wfilter2)
		except sqliteDbAccess.Errors as e:
			return jsonErrorReturn()

		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name=friendshipsMessageName))
