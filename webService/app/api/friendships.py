from bottle import request, response
from bottle import post, get, delete

from api.apiUtils.index import jsonSuccessReturn, jsonErrorReturn
from api.apiUtils.index import ErrorMessage, Errors, getDbConnect


@get('/users/<user_id>/friends')
def listing_handler(user_id):
	'''Handles single user show'''
	# parse input data

	cursor = getDbConnect().cursor()

	user = cursor.execute("SELECT * FROM user WHERE user.id =(?)", (user_id,)).fetchone()
	if(user):
		users = cursor.execute("SELECT user.id, user.username FROM friendship, user WHERE ((friendship.firstFriend =(?) AND friendship.secondFriend = user.id) OR (friendship.secondFriend =(?) AND friendship.firstFriend = user.id))", (user_id, user_id)).fetchall()
		cursor.close()
		return jsonSuccessReturn(users)

	cursor.close()
	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="User"))

@post('/users/<user_id>/friends')
def creation_handler(user_id):
	'''Handles user creation'''

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
		dbConnect = getDbConnect()
		cursor = dbConnect.cursor()
		friendship = cursor.execute("SELECT * FROM friendship WHERE (friendship.firstFriend =(?) AND friendship.secondFriend =(?))", (friend_id, user_id)).fetchone()
		cursor.close()
		if(friendship):
			return jsonErrorReturn(ErrorMessage._existsalready.format(name="Friendship"))

		dbConnect.execute("INSERT INTO friendship(firstFriend, secondFriend) VALUES (?,?)", (user_id, friend_id))
		dbConnect.commit()
	except Errors as e:
		
		dbConnect.rollback()
		return jsonErrorReturn()

	
	return jsonSuccessReturn()


@delete('/users/<user_id>/friends/<friend_id>')
def deletion_handler(user_id, friend_id):
	'''Handles user deletion'''


	dbConnect = getDbConnect()
	cursor = dbConnect.cursor()
	friendship = cursor.execute("SELECT * FROM friendship WHERE ((friendship.firstFriend =(?) AND friendship.secondFriend =(?)) OR (friendship.firstFriend =(?) AND friendship.secondFriend =(?)))", (user_id, friend_id, friend_id, user_id)).fetchone()
	cursor.close()

	if(friendship):
		try:
			dbConnect.execute("DELETE FROM friendship WHERE ((friendship.firstFriend =(?) AND friendship.secondFriend =(?)) OR (friendship.firstFriend =(?) AND friendship.secondFriend =(?)))", (user_id, friend_id, friend_id, user_id))
			dbConnect.commit()
		except Errors as e:
			
			dbConnect.rollback()
			return jsonErrorReturn()

		
		return jsonSuccessReturn()

	return jsonErrorReturn(ErrorMessage._doesntexist.format(name="Friendship"))
