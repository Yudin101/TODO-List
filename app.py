import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if os.path.exists("userData.db") == False:
    with open("userData.db", 'w'):
        pass

db = SQL("sqlite:///userData.db")

db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);")

db.execute("CREATE TABLE IF NOT EXISTS todoList (user_id INTEGER NOT NULL, todos TEXT NOT NULL)")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    account = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]
    
    if request.method == "POST":
        remove = request.form.get("remove")
        db.execute("DELETE FROM todoList WHERE todos = ?", remove)

        return redirect("/")
        
    else:
        todoList = db.execute("SELECT todos FROM todoList WHERE user_id = ?", session["user_id"])
        todoLen = len(todoList)
        return render_template("index.html", account=account, todoList=todoList, todoLen=todoLen)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")

        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        if len(row) > 0:
            return render_template("register.html", error="already")

        if confirmPassword != password:
            return render_template("register.html", error="noMatch")

        hashedPassword = generate_password_hash(password, "pbkdf2", 16)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashedPassword)

        newRow = db.execute("SELECT id FROM users WHERE username=?", username)
        session["user_id"] = newRow[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("login.html", error=True)

        elif not password:
            return render_template("login.html", error=True)

        row = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
            return render_template("login.html", error=True)

        session["user_id"] = row[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    account = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]

    if request.method == "POST":
        todo = request.form.get("todo")

        if not todo:
            return render_template("add.html", error="empty")

        db.execute("INSERT INTO todoList (user_id, todos) VALUES (?, ?)", session["user_id"], todo)

        return redirect("/")
    else:
        return render_template("add.html", account=account)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    account = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]

    if request.method == "POST":
        global edit
        edit = request.form.get("edit")
        return render_template("edit.html", edit=edit, account=account)

    else:
        return redirect("/")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "POST":
        edited = request.form.get("edited")
        db.execute("UPDATE todoList SET todos=? WHERE todos=? AND user_id=?", edited, edit, session["user_id"])
        return redirect("/")

    else:
        return redirect("/")


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


@app.route("/settings")
@login_required
def settings():
    account = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["username"]
    return render_template("settings.html", account=account)


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    account = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["username"]

    if request.method == "POST":
        currentPassword = request.form.get("currentPassword")
        newPassword = request.form.get("newPassword")
        newPasswordConfirm = request.form.get("newPasswordConfirm")

        row = db.execute("SELECT hash FROM users WHERE username = ?", account)
        
        if not check_password_hash(row[0]["hash"], currentPassword):
            return render_template("change.html", account=account, error="noPrevMatch")

        if newPasswordConfirm !=  newPassword:
            return render_template("change.html", account=account, error="noNewMatch")

        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(newPassword, "pbkdf2", 16), account)
        return render_template("change.html", account=account, error="success") # sounds weird lol

    return render_template("change.html", account=account)


@app.route("/about", methods=["GET"])
@login_required
def about():
    account = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["username"]

    return render_template("about.html", account=account)


@app.errorhandler(404)
def invalid_route(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)