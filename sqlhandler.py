import json
import os
import queue
import threading

import pymysql.cursors


class SQLHandler(object):
    def __init__(self):
        self.insert_queue = queue.Queue(1)
        self.conn = pymysql.connect(host=os.environ['CLOUDSQL_CONNECTION_NAME'],
                                    user=os.environ['CLOUDSQL_USER'],
                                    password=os.environ['CLOUDSQL_PASSWORD'],
                                    db=os.environ['CLOUDSQL_DATABASE'],
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    def select(self, queue):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT `content` FROM `messages` ORDER BY id DESC LIMIT 6")
            queue.put(cursor.fetchall())
        return

    def threaded_select(self):
        result = queue.Queue()
        thread = threading.Thread(target=self.select, args=[result])
        thread.start()
        thread.join()
        messages = result.get()
        return json.dumps([message['content'] for message in messages])

    def insert(self, content):
        with self.conn.cursor() as cursor:
            length = cursor.execute("SELECT * FROM `messages`")
            cursor.execute("""INSERT INTO `messages` (`id`, `content`) 
                                 VALUES ({0}, "{1}")""".format(length, content))

    def threaded_insert(self):
        item = self.insert_queue.get()
        self.insert(item)
        self.insert_queue.task_done()

    def submit(self, content):
        self.insert_queue.put(content)
        self.threaded_insert()
        self.conn.commit()
