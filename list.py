#!/usr/bin/python3
import sqlite3

conn = sqlite3.connect("db/rct.db")

c = conn.cursor()

print("People\n------")

c.execute("SELECT email,name FROM person")

rows = c.fetchall()

for row in rows:
    print (row)


print("Requests\n------")

c.execute("SELECT action,email,name,secret FROM request")

rows = c.fetchall()

for row in rows:
    print (row)
