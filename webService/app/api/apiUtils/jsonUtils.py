import json
from bottle import response

def jsonErrorReturn(message="Unknown Error"):
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({"status" : "ERROR", "message": str(message)})

def jsonSuccessReturn(value={}):
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({"status" : "SUCCESS", "data": value})
