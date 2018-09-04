import json
import os
import queue
import threading

import pymysql.cursors

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_IP = os.environ.get('CLOUDSQL_IP')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')


class SQLHandler(object):
    def __init__(self):
        self.insert_queue = queue.Queue(1)
        if os.environ.get('GOOGLE_CLOUD_PROJECT', '') == '':
            self.conn = pymysql.connect(host=CLOUDSQL_IP,
                                        user=CLOUDSQL_USER,
                                        password=CLOUDSQL_PASSWORD,
                                        db=CLOUDSQL_DATABASE,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)
            self.select_key = 'content'
        else:
            self.conn = pymysql.connect(unix_socket=os.path.join('/cloudsql', CLOUDSQL_CONNECTION_NAME),
                                        user=CLOUDSQL_USER,
                                        passwd=CLOUDSQL_PASSWORD,
                                        db=CLOUDSQL_DATABASE)
            self.select_key = 0

    def select(self, queue):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT `content` FROM `messages` ORDER BY id DESC LIMIT 6")
            queue.put(cursor.fetchall())
            cursor.close()
        return

    def threaded_select(self):
        result = queue.Queue()
        thread = threading.Thread(target=self.select, args=[result])
        thread.start()
        thread.join()
        messages = result.get()
        return json.dumps([message[self.select_key] for message in messages])

    def insert(self, content):
        with self.conn.cursor() as cursor:
            length = cursor.execute("SELECT * FROM `messages`")
            cursor.execute("""INSERT INTO `messages` (`id`, `content`) 
                                 VALUES (%s, %s)""", (length, content))
            cursor.close()

    def threaded_insert(self):
        item = self.insert_queue.get()
        self.insert(item)
        self.insert_queue.task_done()

    def submit(self, content):
        self.insert_queue.put(content)
        self.threaded_insert()
        self.conn.commit()
