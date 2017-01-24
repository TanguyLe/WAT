import sqlite3
db = sqlite3.connect('WAT.db')
db.execute("DROP TABLE IF EXISTS friendship")
db.execute("DROP TABLE IF EXISTS user")
db.execute("DROP TABLE IF EXISTS message")
db.execute("DROP TABLE IF EXISTS conversation")
db.execute("DROP TABLE IF EXISTS conversation_participant")
db.commit()
