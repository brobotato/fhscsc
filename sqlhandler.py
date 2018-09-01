import queue
import sqlite3
import threading
import json


class SQLHandler(object):
    def __init__(self, db):
        self.db = db
        self.insert_queue = queue.Queue(1)
        self.conn = sqlite3.connect(self.db, check_same_thread=False)

    def select(self, queue):
        queue.put(self.conn.execute("SELECT content FROM messages").fetchmany(6))
        return

    def threaded_select(self):
        result = queue.Queue()
        thread = threading.Thread(target=self.select, args=[result])
        thread.start()
        thread.join()
        messages = result.get()
        return json.dumps([message[0] for message in messages])

    def insert(self, content):
        length = self.conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        self.conn.execute("""INSERT INTO messages (id, content) 
                             VALUES (?, ?)""", [length, content])

    def threaded_insert(self):
        item = self.insert_queue.get()
        self.insert(item)
        self.insert_queue.task_done()

    def submit(self, content):
        self.insert_queue.put(content)
        self.threaded_insert()
        self.conn.commit()
