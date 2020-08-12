import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure sqlite3 Library to use SQLite database
db = sqlite3.connect('data.db')

# Define global variable
i = 0
lq = []

def many(x):
    s = []
    a = x.lower()
    we2 = '%' + a
    we3 = we2 + '%'
    w = a[0]
    b = w.upper()
    x = b + a[1:]
    we1 = x + '%'
    s.extend([x,we1,we2,we3])
    return s

# @app.route("/")
# def home():
#     return render_template("homepage.html")

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        lq.clear()
        first = request.form.get("first")
        middle = request.form.get("middle")
        last =  request.form.get("last")
        if not last:
            if not first:
                if not middle:
                    return render_template("search.html")
                else:
                    s = many(middle)
                    for x in db.execute("SELECT name, middlename, surname FROM demography WHERE middlename = ? or middlename LIKE ? or middlename LIKE ? or middlename LIKE ?", s):
                        lq.append(x)
            else:
                if not middle:
                    s = many(first)
                    for x in db.execute("SELECT name, middlename, surname FROM demography WHERE name = ? or name LIKE ? or name LIKE ? or name LIKE ?", s):
                        lq.append(x)
                else:
                    s = many(first)
                    s += many(middle)
                    for x in db.execute("SELECT name, middlename, surname FROM demography WHERE (name = ? or name LIKE ? or name LIKE ? or name LIKE ?) and (middlename = ? or middlename LIKE ? or middlename LIKE ? or middlename LIKE ?)", s):
                        lq.append(x)
        else:
            if not first:
                if not middle:
                    s = many(last)
                    for x in db.execute("SELECT name, middlename, surname FROM demography WHERE surname = ? or surname LIKE ? or surname LIKE ? or surname LIKE ?", s):
                        lq.append(x)
                else:
                    s = many(last)
                    s += many(middle)
                    for x in db.execute("SELECT name, middlename, surname FROM demography WHERE (surname = ? or surname LIKE ? or surname LIKE ? or surname LIKE ?) and (middlename = ? or middlename LIKE ? or middlename LIKE ? or middlename LIKE ?)", s):
                        lq.append(x)
            else:
                if not middle:
                    s = many(last)
                    s += many(first)
                    for x in db.execute("SELECT name, middlename, surname FROM demography WHERE (surname = ? or surname LIKE ? or surname LIKE ? or surname LIKE ?) and (name = ? or name LIKE ? or name LIKE ? or name LIKE ?)", s):
                        lq.append(x)
                else:
                    s = many(last)
                    s += many(middle)
                    s += many(first)
                    for x in db.execute("SELECT name, middlename, surname FROM demography WHERE (surname = ? or surname LIKE ? or surname LIKE ? or surname LIKE ?) and (middlename = ? or middlename LIKE ? or middlename LIKE ? or middlename LIKE ?) and (name = ? or name LIKE ? or name LIKE ? or name LIKE ?)", s):
                        lq.append(x)
        if not lq:
            return redirect("/")
        else:
            return render_template("result.html", q = lq)

@app.route("/name/<q>")
def name(q):
    x = []
    s = q.split()
    if len(s) == 2:
        w = s[1]
        s[1] = ''
        s.append(w)

    for j in db.execute("SELECT name, middlename, surname, DOB, age, gender, marital_status FROM demography WHERE name = ? and middlename = ? and surname = ?", s):
        x.append(j)
    return render_template("result.html", j = x, c = "name")

@app.route("/family/<q>")
def family(q):
    s = q.split()
    if len(s) == 2:
        w = s[1]
        s[1] = ''
        s.append(w)


    for row in db.execute("SELECT family_no FROM demography WHERE name = ? and middlename = ? and surname = ?", s):
        r = row
    j = db.execute("SELECT name, middlename, surname, DOB, age, gender, marital_status FROM demography WHERE family_no = ?", r)
    return render_template("result.html", j = j, c = "family")

@app.route("/age", methods=["POST"])
def age():
    lq.clear()
    gender = (request.form.get('gender'),)
    age1 = (request.form.get('age1'),)
    age2 = (request.form.get('age2'),)
    s = []
    if not gender[0]:
        if age1[0] == '':
            if age2[0] == '':
                return render_template("search.html")
            else:
                for x in db.execute("SELECT name, middlename, surname FROM demography WHERE age <= ?", age2):
                    lq.append(x)
        else:
            if age2[0] == '':
                for x in db.execute("SELECT name, middlename, surname FROM demography WHERE age >= ?", age1):
                    lq.append(x)
            else:
                s.append(age1[0])
                s.append(age2[0])
                for x in db.execute("SELECT name, middlename, surname FROM demography WHERE age >= ? and age <= ?", s):
                    lq.append(x)
    else:
        if age1[0] == '':
            if age2[0] == '':
                for x in db.execute("SELECT name, middlename, surname FROM demography WHERE gender = ?", gender):
                    lq.append(x)
            else:
                s.append(gender[0])
                s.append(age2[0])
                for x in db.execute("SELECT name, middlename, surname FROM demography WHERE gender = ? and age <= ?", s):
                    lq.append(x)
        else:
            if age2[0] == '':
                s.append(gender[0])
                s.append(age1[0])
                for x in db.execute("SELECT name, middlename, surname FROM demography WHERE gender = ? and age >= ?", s):
                    lq.append(x)
            else:
                s.append(gender[0])
                s.append(age1[0])
                s.append(age2[0])
                for x in db.execute("SELECT name, middlename, surname FROM demography WHERE gender = ? and age >= ? and age <= ?", s):
                    lq.append(x)
    if not lq:
            return redirect("/")
    else:
        return render_template("result.html", q = lq)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("familyno") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def capital(x):
    a = x.lower()
    w = a[0]
    b = w.upper()
    x = b + a[1:]
    return x

def date(t):
    x = t.split("/")
    if len(x) == 3:
        if x[0].isdigit() == True and x[1].isdigit() == True and x[2].isdigit() == True:
            if len(x[2]) == 4 and int(x[2]) % 4 == 0:
                if int(x[1]) in (1,3,5,7,8,10,12):
                    if int(x[0]) >= 1 and int(x[0]) <= 31:
                        return t
                elif int(x[1]) in (4,6,9,11):
                    if int(x[0]) >= 1 and int(x[0]) <= 30:
                        return t
                elif int(x[1]) == 2:
                    if int(x[0]) >= 1 and int(x[0]) <= 29:
                        return t
            elif len(x[2]) == 4:
                if int(x[1]) in (1,3,5,7,8,10,12):
                    if int(x[0]) >= 1 and int(x[0]) <= 31:
                        return t
                elif int(x[1]) in (4,6,9,11):
                    if int(x[0]) >= 1 and int(x[0]) <= 30:
                        return t
                elif int(x[1]) == 2:
                    if int(x[0]) >= 1 and int(x[0]) <= 28:
                        return t
    y = ""
    return y

@app.route("/update", methods=["POST"])
@login_required
def update():
    s = []
    head = request.form.get("head")
    g = 1
    for i in db.execute("SELECT id FROM demography WHERE family_no = ?", session["familyno"]):
        s.clear()
        t = request.form.get(f"first{ g }")
        s.append(capital(t))
        t = request.form.get(f"middle{ g }")
        s.append(capital(t))
        t = request.form.get(f"last{ g }")
        s.append(capital(t))
        t = request.form.get(f"DOB{ g }")
        s.append(date(t))
        t = request.form.get(f"age{ g }")
        if t.isdigit() == True:
            if int(t) > 0:
                s.append(t)
            else:
                s.append("")
        else:
            s.append("")
        t = request.form.get(f"gender{ g }")
        s.append(t)
        t = request.form.get(f"marital{ g }")
        s.append(t)
        if g == int(head):
            s.append("H")
        else:
            s.append("")
        s.append(f"{i[0]}")
        g += 1
        db.execute("UPDATE demography SET name = ?, middlename = ?, surname = ?, DOB = ?, age = ?, gender = ?, marital_status = ?, head = ? WHERE id = ?", s)
        db.commit()
    return redirect("/logout")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        lq.clear()
        s = []
        x = []
        first = request.form.get("first")
        middle = request.form.get("middle")
        last = request.form.get("last")
        last = capital(last)
        middle = capital(middle)
        first = capital(first)
        s.extend([first,middle,last])
        for r in db.execute("SELECT family_no FROM demography WHERE name = ? and middlename >= ? and surname <= ? and head='H'", s):
            x.append(r)
        if not x:
            return render_template("search.html")
        else:
            sa = []
            session["familyno"] = x[0]
            for r in db.execute("SELECT * FROM demography"):
                sa.append(r)
            session["PEOPLE"] = sa[-1][0]
            i = 1
            for d in db.execute("SELECT name, middlename, surname, DOB, age, gender, marital_status, head FROM demography WHERE family_no = ?", x[0]):
                l = list(d)
                l.append(i)
                d = tuple(l)
                i += 1
                lq.append(d)
            session["i"] = i - 1
            return render_template("update.html", q = lq)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        first = request.form.get("first")
        middle = request.form.get("middle")
        last = request.form.get("last")
        DOB = request.form.get("DOB")
        age = request.form.get("age")
        gender = request.form.get("gender")
        marital = request.form.get("marital")
        if first == '' and middle == '' and last == '' and DOB == '' and age == '' and gender == None and marital == None:
            lq.clear()
            i = 1
            for d in db.execute("SELECT name, middlename, surname, DOB, age, gender, marital_status, head FROM demography WHERE family_no = ?", session["familyno"]):
                l = list(d)
                l.append(i)
                d = tuple(l)
                i += 1
                lq.append(d)
            return render_template("update.html", q = lq)
        session["PEOPLE"] += 1
        s = [session["PEOPLE"]]
        s += [capital(last)]
        s += [capital(first)]
        s += [capital(middle)]
        s += [date(DOB)]
        if age.isdigit() == True:
            if int(age) > 0:
                s += [age]
            else:
                s += [age]
        else:
            s += [age]
        if gender == 'M' or gender == 'F':
            s += [gender]
        else:
            s += ['']
        if marital == 'M' or marital == 'U':
            s += [marital]
        else:
            s += ['']
        out = session["familyno"][0]
        s += [out]
        s += ['']
        db.execute("INSERT INTO demography (id, surname, name, middlename, DOB, age, gender, marital_status, family_no, head) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", s)
        db.commit()
        lq.clear()
        i = 1
        for d in db.execute("SELECT name, middlename, surname, DOB, age, gender, marital_status, head FROM demography WHERE family_no = ?", session["familyno"]):
            l = list(d)
            l.append(i)
            d = tuple(l)
            i += 1
            lq.append(d)
        return render_template("update.html", q = lq)

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "GET":
        lq.clear()
        for f in db.execute("SELECT name, middlename FROm demography WHERE family_no = ?", session["familyno"]):
            lq.append(f)
        return render_template("remove.html", q = lq)
    else:
        remove = request.form.get("remove")
        s = remove.split(" ")
        s.append(session["familyno"][0])
        db.execute("DELETE FROM demography WHERE name = ? and middlename = ? and family_no = ?", s)
        db.commit()
        session["PEOPLE"] -= 1
        lq.clear()
        i = 1
        for d in db.execute("SELECT name, middlename, surname, DOB, age, gender, marital_status, head FROM demography WHERE family_no = ?", session["familyno"]):
            l = list(d)
            l.append(i)
            d = tuple(l)
            i += 1
            lq.append(d)
        return render_template("update.html", q = lq)