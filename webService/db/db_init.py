import db_clean
import sqlite3
db = sqlite3.connect('WAT.db')
db.execute("CREATE TABLE users (username CHAR(100) PRIMARY KEY, password CHAR(100) NOT NULL)")
db.execute("INSERT INTO users VALUES ('Marc', 'lol')")
db.execute("INSERT INTO users VALUES ('Theo', 'smartPass')")
db.execute("INSERT INTO users VALUES ('Jean', 'password')")
db.commit()
