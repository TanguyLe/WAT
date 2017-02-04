from bottle import request, response
from bottle import post, get, delete, static_file

from api import apiUtils

@get('/help')
def helping_handler():
	'''Handles user creation'''   
	return static_file("help.html", root='./static/')
