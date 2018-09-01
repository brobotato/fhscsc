import os

import pymysql

conn = pymysql.connect(host=os.environ['CLOUDSQL_CONNECTION_NAME'],
                       user=os.environ['CLOUDSQL_USER'],
                       password=os.environ['CLOUDSQL_PASSWORD'],
                       db=os.environ['CLOUDSQL_DATABASE'],
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

conn.cursor().execute("""CREATE TABLE `messages`
                (
                `id` int(11) ,
                `content` varchar(255),
                PRIMARY KEY (`id`)
                );""")
