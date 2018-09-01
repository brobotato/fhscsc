import sqlite3

conn = sqlite3.connect("messages.db")

conn.execute("""CREATE TABLE messages
                (
                id int,
                content varchar(255)
                );""")