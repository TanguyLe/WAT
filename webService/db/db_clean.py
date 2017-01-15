import sqlite3
db = sqlite3.connect('WAT.db')
db.execute("DROP TABLE IF EXISTS users")
db.commit()
