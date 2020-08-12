import sqlite3

v = (10,)
db = sqlite3.connect('data.db')
s = []
for row in db.execute("SELECT name, middlename, surname FROM demography WHERE age <= '0'"):
    s.append(row)
for r in range(len(s)):
    print(s[r])