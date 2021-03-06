import sqlite3
from api.utils.logManager import LogManager
from api.constants.index import LOG_FULL_SQLITE_QUERY, LOG_SQLITE, LOG_UN_LOGGING


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteDbAccess:
    IntegrityError = sqlite3.IntegrityError
    ProgrammingError = sqlite3.ProgrammingError
    Error = sqlite3.Error

    @staticmethod
    def create_service(path="../db/WAT.db", main_table=None, logging=True):

        dbaccess = sqlite3.connect(path)

        if not logging:
            LogManager.info_log(LOG_SQLITE + LOG_UN_LOGGING)

        if logging:
            LogManager.info_log(LOG_SQLITE + "Connection to the database")

        dbaccess.execute("PRAGMA foreign_keys = ON")
        dbaccess.commit()

        if logging:
            LogManager.info_log(LOG_SQLITE + "Enabling foreign keys")

        dbaccess.row_factory = dict_factory

        return SqliteDbAccess(dbaccess, main_table=main_table, logging=logging)

    def __init__(self, dbaccess, main_table=None, logging=True):

        if not isinstance(dbaccess, sqlite3.Connection):
            LogManager.error_log(LOG_SQLITE + "dbaccess must be an instance of Connection sqlite3 class")
            raise TypeError("dbaccess must be an instance of Connection sqlite3 class")

        self._dbaccess = dbaccess
        self._main_table = main_table
        self._logging = logging

    def exec_and_commit(self, query, commit=True):

        try:
            self._dbaccess.execute(query)
            if commit:
                self._dbaccess.commit()

            if self._logging:
                LogManager.info_log(LOG_FULL_SQLITE_QUERY + query)

        except SqliteDbAccess.Error as e:
            self._dbaccess.rollback()

            if type(e) == sqlite3.OperationalError:
                e.type = "PROGRAMMING_ERROR"
            elif type(e) == sqlite3.IntegrityError:
                e.type = "INTEGRITY_ERROR"
            else:
                e.type = "UNKNOWN_ERROR"

            if self._logging:
                LogManager.error_log(LOG_SQLITE + "Rollback, error : " + str(e))

            raise e

    def get(self, table=None, w_filter=None, multiple=True):

        if not table:
            table = self._main_table
        w_string = (" WHERE " + w_filter) if w_filter else ''
        query = "SELECT * FROM " + table + w_string
        result = self._dbaccess.cursor().execute(query)

        if self._logging:
            LogManager.info_log(LOG_FULL_SQLITE_QUERY + query)

        if multiple:
            result = result.fetchall()
        else:
            result = result.fetchone()

        return result

    def get_last(self, table=None, attribute="id"):

        if not table:
            table = self._main_table

        query_string = "SELECT * FROM " + table + " ORDER BY " + attribute + " DESC LIMIT 1"
        if self._logging:
            LogManager.info_log(LOG_FULL_SQLITE_QUERY + query_string)

        return self._dbaccess.cursor().execute(query_string).fetchone()

    def get_join(self, params=None, w_filter=None, distinct=True):
        """Be careful, works only with 2 tables provided"""

        if not params:
            params = {}

        wstring = (" WHERE " + w_filter + " AND ") if w_filter else ""

        tables_names_string = ''
        return_attributes_string = ''
        w_filter_join_string = '('

        for table in params.keys():
            tables_names_string += table + ", "
            for attribute in params[table]["attributes"]:
                return_attributes_string += (table + "." + attribute + ", ")
            w_filter_join_string += (table + "." + params[table]["join"] + "=")

        tables_names_string = tables_names_string[:-2]
        return_attributes_string = return_attributes_string[:-2]
        w_filter_join_string = w_filter_join_string[:-1] + ')'

        wstring += w_filter_join_string
        select_string = "SELECT DISTINCT " if distinct else "SELECT"
        final_query_string = select_string + return_attributes_string + " FROM " + tables_names_string + wstring

        if self._logging:
            LogManager.info_log(LOG_FULL_SQLITE_QUERY + final_query_string)

        return self._dbaccess.cursor().execute(final_query_string).fetchall()

    def insert(self, table=None, params=None, commit=True, get_last_attribute=None):

        if not params:
            params = {}

        if not table:
            table = self._main_table

        tables_string = table + '('
        values_string = '('
        for attribute in params.keys():
            tables_string += attribute + ", "
            values_string += (("'" + params[attribute] + "', ")
                              if type(params[attribute]) == str
                              else str(params[attribute]) + ", ")

        tables_string = tables_string[:-2] + ')'
        values_string = values_string[:-2] + ')'

        self.exec_and_commit(query=("INSERT INTO " + tables_string + " VALUES" + values_string), commit=commit)

        if get_last_attribute:
            if type(get_last_attribute) == str:
                return self.get_last(table=table, attribute=get_last_attribute)
            else:
                return self.get_last(table=table)

    def update(self, table=None, s_filter=None, w_filter=None, commit=True):

        if not table:
            table = self._main_table

        w_string = (" WHERE " + w_filter) if w_filter else ""

        self.exec_and_commit(query=("UPDATE " + table + " SET " + s_filter + w_string), commit=commit)

    def delete(self, table=None, w_filter=None, commit=True):

        if not table:
            table = self._main_table

        w_string = (" WHERE " + w_filter) if w_filter else ""

        self.exec_and_commit(query=("DELETE FROM " + table + w_string), commit=commit)

    def __del__(self):
        if self._logging:
            LogManager.info_log(LOG_SQLITE + "Closing database connection")
        self._dbaccess.close()
