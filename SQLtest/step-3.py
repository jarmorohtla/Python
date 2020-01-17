# File name: step-3.py
# Author: Jarmo Rohtla
# Python Version: 3.7.5

import psycopg2
from tkinter import *

def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    product_id = value[value.index(':')+1 : value.index(')')]
    conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPassword, host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute('''SELECT name, count(*) AS "popularity"
                from order_lines
                join products on order_lines.product_id = products.id
                where order_id IN ( SELECT order_id from order_lines WHERE product_id=''' + product_id + ''' )
                AND product_id <> ''' + product_id + ''' 
                GROUP BY name
                ORDER BY popularity DESC''');
    rows = cur.fetchall()
    txtRelatedProducts.delete("1.0", END)
    txtRelatedProducts.insert(INSERT, "Related products of " + value[0 : value.index('(')] + "\n")
    for row in rows:
        txtRelatedProducts.insert(INSERT, str(row[1]) + ": " + row[0] + "\n")
    conn.close()


dbName = "avalahdb"
dbUser = "avalah"
dbPassword = "avalah"
conn = psycopg2.connect(database=dbName, user=dbUser, password=dbPassword, host="127.0.0.1", port="5432")
cur = conn.cursor()

top = Tk()
top.wm_title("Products")
LbProducts = Listbox(top, height=20, width=40, bd=5, selectmode="SINGLE")
txtRelatedProducts = Text ( top, height=21, width=40, bd=5 )

cur.execute("SELECT id,name from products");
rows = cur.fetchall()
for row in rows:
   LbProducts.insert(END, row[1] + " (id: " + str(row[0]) + ")")
LbProducts.pack(side=LEFT)
LbProducts.bind('<<ListboxSelect>>', onselect)
txtRelatedProducts.pack(side=LEFT)
txtRelatedProducts.insert(INSERT, "Click on product to see related products")
top.mainloop()
conn.close()