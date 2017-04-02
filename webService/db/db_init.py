import db_clean
import sqlite3

db = sqlite3.connect('WAT.db')
db.execute(
    "CREATE TABLE user (id INTEGER PRIMARY KEY, username CHAR(100) NOT NULL UNIQUE, password CHAR(100) NOT NULL)")
db.execute("INSERT INTO user(username, password) VALUES ('Marc', 'lol')")
db.execute("INSERT INTO user(username, password) VALUES ('Theo', 'smartPass')")
db.execute("INSERT INTO user(username, password) VALUES ('Jean', 'password')")
db.execute("INSERT INTO user(username, password) VALUES ('Pierre', 'password3')")
db.execute("INSERT INTO user(username, password) VALUES ('Etienne', 'password4')")
db.execute("INSERT INTO user(username, password) VALUES ('Paul', 'password4')")

db.execute(
    '''CREATE TABLE friendship (
            firstFriend INTEGER NOT NULL,
            secondFriend INTEGER NOT NULL,

            PRIMARY KEY(firstFriend, secondFriend),
            FOREIGN KEY(firstFriend) REFERENCES user(id),
            FOREIGN KEY(secondFriend) REFERENCES user(id))
    '''
)
db.execute("INSERT INTO friendship VALUES (1,2)")
db.execute("INSERT INTO friendship VALUES (2,1)")
db.execute("INSERT INTO friendship VALUES (1,3)")
db.execute("INSERT INTO friendship VALUES (3,1)")
db.execute("INSERT INTO friendship VALUES (1,4)")
db.execute("INSERT INTO friendship VALUES (4,1)")
db.execute("INSERT INTO friendship VALUES (1,5)")
db.execute("INSERT INTO friendship VALUES (5,1)")
db.execute("INSERT INTO friendship VALUES (2,3)")
db.execute("INSERT INTO friendship VALUES (3,2)")
db.execute("INSERT INTO friendship VALUES (5,3)")
db.execute("INSERT INTO friendship VALUES (3,5)")
db.execute("INSERT INTO friendship VALUES (4,5)")
db.execute("INSERT INTO friendship VALUES (5,4)")

db.execute("CREATE TABLE conversation (id INTEGER PRIMARY KEY, name CHAR(100) NOT NULL)")
db.execute("INSERT INTO conversation(name) VALUES ('Picoloc')")
db.execute("INSERT INTO conversation(name) VALUES ('Malaga')")
db.execute("INSERT INTO conversation(name) VALUES ('Fb')")
db.execute("INSERT INTO conversation(name) VALUES ('Smash')")

db.execute(
    '''CREATE TABLE conversation_participant (
                conversation INTEGER NOT NULL,
                user INTEGER NOT NULL, PRIMARY KEY(conversation, user),

                FOREIGN KEY(conversation) REFERENCES conversation(id),
                FOREIGN KEY(user) REFERENCES user(id))
    '''
)
db.execute("INSERT INTO conversation_participant VALUES (1,2)")
db.execute("INSERT INTO conversation_participant VALUES (1,3)")
db.execute("INSERT INTO conversation_participant VALUES (1,4)")
db.execute("INSERT INTO conversation_participant VALUES (1,5)")
db.execute("INSERT INTO conversation_participant VALUES (2,3)")
db.execute("INSERT INTO conversation_participant VALUES (4,3)")
db.execute("INSERT INTO conversation_participant VALUES (4,5)")

db.execute(
    '''CREATE TABLE message (
            id INTEGER PRIMARY KEY,
            content TEXT,
            createdDate DATETIME default current_timestamp,
            conversation INTEGER NOT NULL,
            user INTEGER NOT NULL,

            FOREIGN KEY(user, conversation) REFERENCES conversation_participant(user, conversation))
    '''
)
db.execute("INSERT INTO message(content, conversation, user) VALUES ('Hello you', 1, 3)")
db.execute("INSERT INTO message(content, conversation, user) VALUES ('Hello you', 1, 2)")

db.execute(
    '''CREATE TABLE position (
            id INTEGER PRIMARY KEY,
            position CHAR(100),
            createdDate DATETIME default current_timestamp,
            user INTEGER NOT NULL,

            FOREIGN KEY (user) REFERENCES user(id))
    '''
)
db.execute("INSERT INTO position(position, user) VALUES ('Dtc', 1)")
db.execute("INSERT INTO position(position, user) VALUES ('Dtc2', 1)")
db.execute("INSERT INTO position(position, user) VALUES ('Dtc3', 1)")
db.execute("INSERT INTO position(position, user) VALUES ('Dtc', 2)")
db.commit()
