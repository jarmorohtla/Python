# File name: step-2.py
# Author: Jarmo Rohtla
# Python Version: 3.7.5

import psycopg2
from random import randint

dbName = "avalahdb"
dbUser = "avalah"
dbPassword = "avalah"
conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPassword, host="127.0.0.1", port="5432")
cur = conn.cursor()

i = 1
while i <= 20:
    cur.execute('''INSERT INTO PRODUCTS (ID,NAME) 
                   VALUES (DEFAULT, 'Product ''' + str(i) + '''' );''');
    i += 1

i = 1
while i <= 10:
    cur.execute('''INSERT INTO ORDERS (ID) 
                   VALUES (DEFAULT);''');
    i += 1

i = 1
while i <= 10:
    j = 1
    while j <= 20:
        if randint(1, 10) < 7: 
            cur.execute('''INSERT INTO ORDER_LINES (ID,ORDER_ID,PRODUCT_ID,QUANTITY) 
                           VALUES (DEFAULT, ''' + str(i) + ''', ''' + str(j) + ''', ''' + str(randint(1, 30)) + ''');''');
        j += 1
    i += 1

conn.commit()
conn.close()