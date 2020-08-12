v = "SONI"
a = v.lower()
w = a[0]
b = w.upper()
z = b + a[1:]
from cs50 import SQL
db = SQL("sqlite:///data.db")
q = db.execute("SELECT name, middlename, surname FROM demography WHERE surname = ? and head='H' ", z)
for s in q:
    if s["middlename"] == '':
        print(f"{s['name']} {s['surname']}")
    else:
        print(f"{s['name']} {s['middlename']} {s['surname']}")