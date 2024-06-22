import os
import secrets

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import date, timedelta

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours = 24)
app.config["SECRET_KEY"] = secrets.token_urlsafe(32)
Session(app)

# Checking if userData.db exists
if os.path.exists("userData.db") == False:
    with open("userData.db", 'w'):
        pass

db = SQL("sqlite:///userData.db")

# Creating the tables
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);")

db.execute("CREATE TABLE IF NOT EXISTS todoList (user_id INTEGER NOT NULL, todos TEXT NOT NULL, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, dat TEXT, tim TEXT);")


# Function to ensure user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Function to redirect user to / if logged in
def logged_in():
    if session.get("user_id"):
        return True
    return False


# Index Page
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    todoCount = db.execute("SELECT COUNT(todos) FROM todoList WHERE user_id=?", session["user_id"])[0]["COUNT(todos)"]
    
    # POST method in index is to delete the tasks
    if request.method == "POST":
        remove = request.form.get("remove")
        db.execute("DELETE FROM todoList WHERE todos = ?", remove)

        return redirect("/")
        
    else:
        todoList = db.execute("SELECT todos, dat, tim FROM todoList WHERE user_id = ?", session["user_id"])
        todoLen = len(todoList)

        return render_template("index.html", todoCount=todoCount, todoList=todoList, todoLen=todoLen, today=str(date.today()))


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # Checking if the user already exists
        if len(row) > 0:
            return render_template("register.html", error="already")

        hashedPassword = generate_password_hash(password, "pbkdf2", 16)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashedPassword)

        newRow = db.execute("SELECT id FROM users WHERE username=?", username)
        session["user_id"] = newRow[0]["id"]

        return redirect("/")

    else:
        if logged_in():
            return redirect("/")

        return render_template("register.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        row = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
            return render_template("login.html", error=True)

        session["user_id"] = row[0]["id"]

        return redirect("/")

    else:
        if logged_in():
            return redirect("/")

        return render_template("login.html")


# Logout
@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect("/")


# Add Task Page
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    todoCount = db.execute("SELECT COUNT(todos) FROM todoList WHERE user_id=?", session["user_id"])[0]["COUNT(todos)"]

    if request.method == "POST":
        todo = request.form.get("todo")
        time = request.form.get("time")
        date = request.form.get("date")

        # Preventing duplicate tasks
        todoList = db.execute("SELECT todos FROM todoList WHERE user_id = ?", session["user_id"])
        for todoListDict in todoList:
            if todo == todoListDict["todos"]:
                return render_template("add.html", todoCount=todoCount, error=True)

        db.execute("INSERT INTO todoList (user_id, todos, dat, tim) VALUES (?, ?, ?, ?)", session["user_id"], todo, date, time)

        return redirect("/")
    else:
        return render_template("add.html", todoCount=todoCount)


# Edit Task Page
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    todoCount = db.execute("SELECT COUNT(todos) FROM todoList WHERE user_id=?", session["user_id"])[0]["COUNT(todos)"]

    if request.method == "POST":
        global edit
        global editTime
        global editDate

        edit = request.form.get("edit")
        editTime = db.execute("SELECT tim FROM todoList WHERE todos=?", edit)[0]["tim"]
        editDate = db.execute("SELECT dat FROM todoList WHERE todos=?", edit)[0]["dat"]

        return render_template("edit.html", edit=edit, editTime=editTime, editDate=editDate, todoCount=todoCount)

    else:
        return redirect("/")


# Edited Task Gets Updated
@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "POST":
        editedTask = request.form.get("editedTask")

        editedTime = request.form.get("editedTime")
        editedDate = request.form.get("editedDate")

        db.execute("UPDATE todoList SET todos=?, dat=?, tim=? WHERE todos=? AND user_id=?", editedTask, editedDate, editedTime, edit, session["user_id"])
        
        return redirect("/")

    else:
        return redirect("/")


# Delete Account
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        password = request.form.get("password")

        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if check_password_hash(row[0]["hash"], password):
            db.execute("DELETE FROM users WHERE id=?", session["user_id"])
            db.execute("DELETE FROM todoList WHERE user_id=?", session["user_id"])

            session.clear()
            return redirect("/")

        else:
            return render_template("delete.html", error="noPrevMatch")

    else: 
        return render_template("delete.html")


# Setting Page
@app.route("/settings")
@login_required
def settings():
    account = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["username"]
    return render_template("settings.html", account=account)


# Change Password
@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    account = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

    if request.method == "POST":
        currentPassword = request.form.get("currentPassword")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")

        row = db.execute("SELECT hash FROM users WHERE username = ?", account)
        
        if not check_password_hash(row[0]["hash"], currentPassword):
            return render_template("change.html", account=account, error="noPrevMatch")

        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(password, "pbkdf2", 16), account)
        return render_template("change.html", account=account, error="success") # sounds weird lol

    return render_template("change.html", account=account)


# About Page
@app.route("/about", methods=["GET"])
@login_required
def about():
    account = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

    return render_template("about.html", account=account)

# Handle 404 Error
@app.errorhandler(404)
def invalid_route(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)