from flask import Flask, render_template, session, request
import sqlite3 as s
from flask_session import Session

from werkzeug.utils import redirect

connection = s.connect("CrimeData.db", check_same_thread=False)

listoftables = connection.execute("SELECT NAME FROM sqlite_master WHERE type='table' AND name= 'CRIME'").fetchall()

if listoftables != []:
    print("Table Already Exist")
else:
    connection.execute('''CREATE TABLE CRIME(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        DESCRIPTION TEXT,
                        REMARKS TEXT,
                        DATE TEXT
                        

                       )''')

    print("Table Created Successfully")

listoftables2 = connection.execute("SELECT NAME FROM sqlite_master WHERE type='table' AND name= 'USER'").fetchall()

if listoftables2 != []:
    print("Table Already Exist")
else:
    connection.execute('''CREATE TABLE USER(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        ADDRESS TEXT,
                        EMAIL TEXT,
                        PHONE INTEGER,
                        PASS TEXT

                       )''')

    print("Table Created Successfully")
App = Flask(__name__)
App.config["SESSION_PERMANENT"] = False
App.config["SESSION_TYPE"] = "filesystem"
Session(App)


@App.route('/')
def home():
    return render_template("home.html")


@App.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == "POST":
        getUser = request.form["uname"]
        getPass = request.form["pass"]
        if getUser == "admin" and getPass == "12345":
            return redirect('/viewallcrime')
        else:
            return render_template("adminlogin.html", status=True)
    else:
        return render_template("adminlogin.html", status=False)


@App.route('/viewallcrime')
def viewAll():
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM CRIME")

    result = cursor.fetchall()
    return render_template("viewallcrime.html", crimes=result)



@App.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    global getEmail
    if request.method == "POST":
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM USER WHERE EMAIL='" + getEmail + "' AND PASS='" + getPass + "'"
        print(query)
        result1 = cursor.execute(query).fetchall()
        if len(result1) > 0:
            for i in result1:
                getName = i[1]
                getId = i[0]
                session["name"] = getName
                session["id"] = getId

            return redirect('/userreport')
        else:
            return render_template("userlogin.html", status=True)

    else:

        return render_template("userlogin.html", status=False)


@App.route('/userregister', methods=['GET', 'POST'])
def userRegister():
    global a
    if request.method == "POST":
        getName = request.form["name"]
        getAdd = request.form["add"]
        getnEmail = request.form["email"]
        getPhone = request.form["pno"]
        getnPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM USER WHERE EMAIL='" + getnEmail + "'"
        print(query)
        result1 = cursor.execute(query).fetchall()
        if len(result1) > 0:
            return render_template("userregister.html", status=True)
        else:
            connection.execute("INSERT INTO USER(NAME, ADDRESS, EMAIL, PHONE, PASS) \
                                                                        VALUES('" + getName + "', '" + getAdd + "', '" + getnEmail + "', " + getPhone + ", '" + getnPass + "')")
            connection.commit()
            print("Inserted Successfully")
            return redirect('/userlogin')
    else:

        return render_template("userregister.html", status=False)



@App.route('/userreport', methods=['GET', 'POST'])
def userreport():
    if request.method == "POST":

        getdes = request.form["des"]
        getrem = request.form["rem"]
        getDate = request.form["date"]

        connection.execute("INSERT INTO CRIME(DESCRIPTION, REMARKS, DATE) \
        VALUES('"+getdes+"', '"+getrem+"', '"+getDate+"')")
        connection.commit()
        print("Inserted Successfully")

    return render_template("userreport.html")



@App.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if request.method == "POST":
        getnName = request.form["name"]
        getnAdd = request.form["add"]
        getnnEmail = request.form["email"]
        getnPhone = request.form["pno"]
        getPass = request.form["pass"]
        try:
            query = "UPDATE USER SET NAME='" + getnName + "', ADDRESS='" + getnAdd + "'\
                            ,EMAIL='" + getnnEmail + "', PHONE=" + getnPhone + ", PASS='" + getPass + "'"
            print(query)
            connection.execute(query)
            connection.commit()
            print("Updated Successfully")
            return redirect("/userreport")
        except Exception as e:
            print(e)

    return render_template("editprofile.html")





@App.route("/updatesearch", methods=["GET", "POST"])
def update_search_patient():
    if request.method == "POST":
        getemail = request.form["email"]
        print(getemail)
        cursor = connection.cursor()
        count = cursor.execute("SELECT * FROM USER WHERE EMAIL='" + getemail+"'")
        result = cursor.fetchall()
        print(len(result))
        return render_template("editprofile.html", search=result)

    return render_template("editprofile.html")


@App.route('/dateview', methods=["GET", "POST"])
def dateview():
    if request.method == "POST":
        getdate = request.form["date"]
        print(getdate)
        cursor = connection.cursor()
        count = cursor.execute("SELECT * FROM CRIME WHERE DATE='" + getdate+"'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exist")
        else:
            return render_template("dateview.html", date=result, status=True)
    else:
        return render_template("dateview.html", date=[], status=False)


@App.route('/guestreport', methods=['GET', 'POST'])
def guestreport():
    if request.method == "POST":

        getdes = request.form["des"]
        getrem = request.form["rem"]
        getDate = request.form["date"]

        connection.execute("INSERT INTO CRIME(DESCRIPTION, REMARKS, DATE) \
        VALUES('"+getdes+"', '"+getrem+"', '"+getDate+"')")
        connection.commit()
        print("Inserted Successfully")
    return render_template("guestreport.html")


if __name__ == "__main__":
    App.run()
