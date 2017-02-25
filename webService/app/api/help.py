from bottle import request, response
from bottle import get, static_file


@get('/help')
def help_handler():
    """Handles user creation"""
    return static_file("help.html", root='./static/')
