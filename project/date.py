import sqlite3
import schedule
import time

db = sqlite3.connect('data.db')
def date():
    for t in db.execute("SELECT DOB, id FROM demography"):
        if t[0] != None:
            x = t[0].split("/")
            if len(x[0]) == 2 and len(x[1]) == 1:
                x[1] = '0' + x[1]
            elif len(x[0]) == 1 and len(x[1]) == 2:
                x[0] = '0' + x[0]
            elif len(x[0]) == 1 and len(x[1]) == 1:
                x[0] = '0' + x[0]
                x[1] = '0' + x[1]
            d = [f"{ x[0] }/{ x[1] }/{ x[2] }"]
            d += [t[1]]
            db.execute("UPDATE demography SET DOB = ? WHERE id = ?", d)
            db.commit()

schedule.every().year.at("00:00").do(date())

while 1:
    schedule.run_pending()
    time.sleep(1)