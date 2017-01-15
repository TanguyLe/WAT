from bottle import response
import sqlite3, json


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d
 
def connectDb():
	connection = sqlite3.connect('../db/WAT.db')
	connection.row_factory = dict_factory
	return connection

def jsonReturn(value):
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(value)
