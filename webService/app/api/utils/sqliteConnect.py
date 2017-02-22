import sqlite3

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


class sqliteDbAccess:

	Errors = sqlite3.Error

	@staticmethod
	def create_service(path="../db/WAT.db", mainTable=None):

		dbaccess = sqlite3.connect(path)

		dbaccess.execute("PRAGMA foreign_keys = ON")
		dbaccess.commit()

		dbaccess.row_factory = dict_factory

		return sqliteDbAccess(dbaccess, mainTable=mainTable)

	def __init__(self, dbaccess, mainTable=None):

		if not isinstance(dbaccess, sqlite3.Connection):
			raise TypeError("dbaccess must be an instance of Connection sqlite3 class")
		self._dbaccess = dbaccess
		self.mainTable = mainTable

	def execandcommit(self, query, commit=True):

		try:
			self._dbaccess.execute(query)
			if(commit):
				self._dbaccess.commit()
		except sqliteDbAccess.Errors as e:
			self._dbaccess.rollback()
			raise e

	def get(self, table=None, wfilter=None, multiple=True):

		if(not(table)):
			table = self.mainTable
		wstring = (" WHERE " + wfilter) if wfilter else ""
		result = self._dbaccess.cursor().execute("SELECT * FROM " + table + wstring)

		if(multiple):
			result = result.fetchall()
		else:
			result = result.fetchone()

		return result

	def getlast(self, table=None, attribute="id"):

		if(not(table)):
			table = self.mainTable

		querystring = "SELECT * FROM " + table + " ORDER BY " + attribute + " DESC LIMIT 1"
		return self._dbaccess.cursor().execute(querystring).fetchone()

	def getjoin(self, params={}, wfilter=None, distinct=True):
		#Be carefull, works only with 2 tables provided

		wstring = (" WHERE " + wfilter + " AND ") if wfilter else ""

		tablesnamesstring = ''
		returnattributesstring = ''
		wfilterjoinstring = '('

		for table in params.keys():
			tablesnamesstring += table + ", "
			for attribute in params[table]["attributes"]:
				returnattributesstring += (table + "." + attribute + ", ")
			wfilterjoinstring += (table + "." + params[table]["join"] + "=")

		tablesnamesstring = tablesnamesstring[:-2]
		returnattributesstring = returnattributesstring[:-2]
		wfilterjoinstring = wfilterjoinstring[:-1] + ')'

		wstring += wfilterjoinstring
		selectstring = "SELECT DISTINCT " if distinct else "SELECT"
		finalquerystring = selectstring + returnattributesstring + " FROM " + tablesnamesstring + wstring
		return self._dbaccess.cursor().execute(finalquerystring).fetchall()

	def insert(self, table=None, dict={}, commit=True):

		if(not(table)):
			table = self.mainTable
			
		tablestring = table + '('
		valuesstring = '('
		for attribute in dict.keys():
			tablestring += attribute + ', '
			valuesstring += (('"' + dict[attribute] + '", ') if type(dict[attribute]) == str else str(dict[attribute]) + ', ')

		tablestring = tablestring[:-2] + ')'
		valuesstring = valuesstring[:-2] + ')'
		self.execandcommit(query=("INSERT INTO " + tablestring + " VALUES" + valuesstring), commit=commit)

	def update(self, table=None, sfilter=None, wfilter=None, commit=True):

		if(not(table)):
			table = self.mainTable

		wstring = (" WHERE " + wfilter) if wfilter else ""
		
		self.execandcommit(query=("UPDATE " + table + " SET " + sfilter + wstring), commit=commit)

	def delete(self, table=None, wfilter=None, commit=True):
		
		if(not(table)):
			table = self.mainTable

		wstring = (" WHERE " + wfilter) if wfilter else ""

		self.execandcommit(query=("DELETE FROM " + table + wstring), commit=commit)

	def __del__(self):
		self._dbaccess.close()

Errors = sqlite3.Error