import xlrd
import datetime
from cs50 import SQL

db = SQL("sqlite:///data.db")
# db.execute("CREATE TABLE 'demography' ('id' INTEGER, 'surname' TEXT, 'name' TEXT, 'middlename' TEXT, 'DOB' DATE, 'age' INTEGER, 'gender' VARCHAR(1), 'marital_status' VARCHAR(1), 'family_no' INTEGER, 'head' VARCHAR(1))")
loc = ("excel/Bisa Humad Jain Samaj 2007.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(2)
a = sheet.nrows
for i in range(1, a):
    b = sheet.row_values(i)
    if b[5] == '':
        db.execute("INSERT INTO demography (id, surname, name, middlename, age, gender, marital_status, family_no, head) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", b[0], b[1], b[2], b[3], b[9], b[10], b[12], b[13], b[14])
    else:
        s = xlrd.xldate.xldate_as_tuple(b[5], 0)
        x = f"{s[2]}/{s[1]}/{s[0]}"
        db.execute("INSERT INTO demography (id, surname, name, middlename, DOB, age, gender, marital_status, family_no, head) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", b[0], b[1], b[2], b[3], x, b[9], b[10], b[12], b[13], b[14])