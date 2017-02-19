import sqlite3
from api.apiUtils.genUtils import dict_factory

def getDbConnect():
	dbaccess = sqlite3.connect('../db/WAT.db')
	dbaccess.row_factory = dict_factory
	return dbaccess
	

class sqliteDbAccess:

	Errors = sqlite3.Error

	@staticmethod
	def create_service(path="../db/WAT.db"):
		dbaccess = sqlite3.connect(path)
		dbaccess.row_factory = dict_factory
		return sqliteDbAccess(dbaccess)

	def __init__(self, dbaccess):
		if not isinstance(dbaccess, sqlite3.Connection):
			raise TypeError("dbaccess must be an instance of Connection sqlite3 class")
		self._dbaccess = dbaccess

	def execandcommit(self, query, commit=True):
		try:
			self._dbaccess.execute(query)
			if(commit):
				self._dbaccess.commit()
		except sqliteDbAccess.Errors as e:
			self._dbaccess.rollback()
			raise e

	def get(self, table, wfilter=None):
		wstring = (" WHERE " + wfilter) if wfilter else ""
		result = self._dbaccess.cursor().execute("SELECT * FROM " + table + wstring).fetchall()

		return result

	def insert(self, table, dict, commit=True):
		tablestring = table + '('
		valuesstring = '('
		for attribute in dict.keys():
			tablestring += attribute + ', '
			valuesstring += '"' + dict[attribute] + '", '

		tablestring = tablestring[:-2] + ')'
		valuesstring = valuesstring[:-2] + ')'

		self.execandcommit(query=("INSERT INTO " + tablestring + " VALUES " + valuesstring), commit=commit)

	def update(self, table, sfilter, wfilter=None, commit=True):
		wstring = (" WHERE " + wfilter) if wfilter else ""
		
		self.execandcommit(query=("UPDATE " + table + " SET " + sfilter + wstring), commit=commit)

	def delete(self, table, wfilter=None, commit=True):
		wstring = (" WHERE " + wfilter) if wfilter else ""

		self.execandcommit(query=("DELETE FROM " + table + wstring), commit=commit)

	def __del__(self):
		self._dbaccess.close()

Errors = sqlite3.Error