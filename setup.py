import os

import pymysql

ssl = {'cert': 'ssl/client-cert.pem', 'key': 'ssl/client-key.pem'}
conn = pymysql.connect(host=os.environ['CLOUDSQL_CONNECTION_NAME'],
                       user=os.environ['CLOUDSQL_USER'],
                       password=os.environ['CLOUDSQL_PASSWORD'],
                       db=os.environ['CLOUDSQL_DATABASE'],
                       ssl=ssl,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

conn.cursor().execute("""CREATE TABLE `messages`
                (
                `id` int(11) ,
                `content` varchar(255),
                PRIMARY KEY (`id`)
                );""")
