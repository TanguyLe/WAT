from bottle import request, response
from bottle import post, get, delete

from api import apiUtils

#TODO Generalize requests
@get('/friendships/<id>')
def show_handler(id):
	'''Handles single user show'''
	# parse input data

	c = apiUtils.connectDb().cursor()

	user = c.execute("SELECT * FROM user WHERE user.id =(?)", (id,)).fetchone()
	if(user):
		data = c.execute("SELECT user.id, user.username FROM friendship, user WHERE ((friendship.firstFriend =(?) AND friendship.secondFriend = user.id) OR (friendship.secondFriend =(?) AND friendship.firstFriend = user.id))", (id,id)).fetchall()
		c.close()
		return apiUtils.jsonReturn(data)

	c.close()
	response.status = "400 User doesn't exist"
	return


@post('/friendships')
def creation_handler():
	'''Handles user creation'''

	try:
		try:
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		firstFriend = data['firstFriend']
		secondFriend = data['secondFriend']	

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	try:
		c = apiUtils.connectDb()
		c.execute("INSERT INTO friendship(firstFriend, secondFriend) VALUES (?,?)", (firstFriend, secondFriend))
		c.commit()
	except apiUtils.Errors as e:
		#TODO Precise error handling as things are going to get more complex there
		c.rollback()
		response.status = "400 Friendship exists already"
		return

	#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
	return apiUtils.jsonReturn({"status": "SUCCESS"})

@delete('/friendships')
def deletion_handler():
	'''Handles user deletion'''

	try:
		try:
			data = request.query
		except:
			raise ValueError

		if data is None:
			raise ValueError

		firstFriend = data['firstFriend']
		secondFriend = data['secondFriend']	

	except ValueError:
		response.status = "400 Value Error"
		return

	except KeyError:
		response.status = "400 Key Error"
		return

	c = apiUtils.connectDb()
	cursor = c.cursor()
	data = cursor.execute("SELECT * FROM friendship WHERE (friendship.firstFriend =(?) AND friendship.secondFriend =(?))", (firstFriend, secondFriend)).fetchone()
	cursor.close()

	if(data):
		try:
			c.execute("DELETE FROM friendship WHERE (friendship.firstFriend =(?) AND friendship.secondFriend =(?))", (firstFriend, secondFriend))
			c.commit()
		except apiUtils.Errors as e:
			#TODO Precise error handling as things are going to get more complex there
			c.rollback()
			response.status = "400 Unknow error"
			return

		#TODO Should we return something else ? Format our api returns, status is in the response.status (Or is it not ?)
		return apiUtils.jsonReturn({"status": "SUCCESS"})

	response.status = "400 Friendship doesn't exist"
	return
