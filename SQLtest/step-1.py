# File name: step-1.py
# Author: Jarmo Rohtla
# Python Version: 3.7.5

import psycopg2

dbName = "avalahdb"
dbUser = "avalah"
dbPassword = "avalah"
conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPassword, host="127.0.0.1", port="5432")
cur = conn.cursor()

cur.execute('''CREATE TABLE PRODUCTS
               (ID SERIAL PRIMARY KEY NOT NULL,
               NAME TEXT NOT NULL);''')

cur.execute('''CREATE TABLE ORDERS
               (ID SERIAL PRIMARY KEY NOT NULL);''')

cur.execute('''CREATE TABLE ORDER_LINES
               (ID SERIAL PRIMARY KEY NOT NULL,
               ORDER_ID integer NOT NULL,
               PRODUCT_ID integer NOT NULL,
               QUANTITY integer NOT NULL);''')

conn.commit()
conn.close()