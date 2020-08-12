import schedule
import time
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

db = sqlite3.connect('data.db')

def age():
    for s in db.execute("SELECT DOB, id FROM demography"):
        if s[0] != None:
            w = datetime.date(datetime.strptime(s[0], '%d/%m/%Y'))
            x = datetime.now()
            t = timedelta(minutes=30,hours=5)
            y = x + t
            z = datetime.date(y)
            rdelta = relativedelta(z,w)
            d = list(s)
            d[0] = rdelta.years
            db.execute("UPDATE demography SET age = ? WHERE id = ?", d)
            db.commit()

schedule.every().day.at("00:00").do(age())

while 1:
    schedule.run_pending()
    time.sleep(1)