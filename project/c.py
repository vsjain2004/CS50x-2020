import sqlite3

db = sqlite3.connect('data.db')
s = []
for row in db.execute("SELECT * from demography WHERE middlename LIKE 'G%' or middlename LIKE '%g%' or middlename LIKE '%g' or middlename = 'G'"):
    s.append(row)
# s.append(db.execute("SELECT * from demography WHERE middlename LIKE '%g%'"))
# s.append(db.execute("SELECT * from demography WHERE middlename LIKE '%g'"))
# s.append(db.execute("SELECT * from demography WHERE middlename = 'G'"))
print(s[0][0])