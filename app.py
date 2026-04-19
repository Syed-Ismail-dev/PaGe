from flask import Flask, render_template, session, request, redirect
from cs50 import SQL
from helper import login_required, is_strong_password
from flask_session import Session
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet


load_dotenv()

key = os.getenv("SECRET_KEY").encode()
f = Fernet(key)

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///password.db")


# ************************************** INDEX / HOME ROUTE *******************************************

@app.route("/")
def index():
    if "user_id" in session:
        datas = db.execute(
            "SELECT id, accountname, accountpassword  FROM passwords WHERE user_id = ?",
            session["user_id"]
        )
        for row in datas:
            row["accountpassword"] = f.decrypt(row["accountpassword"]).decode()
        return render_template("home.html", datas=datas)
    return render_template("index.html")


# ************************************** SAVE ROUTE ******************************************************

@app.route("/save", methods=["POST"])
@login_required
def save():
    if request.method == "POST":

        db.execute(
            "INSERT INTO passwords (user_id, accountname, accountpassword) VALUES (?, ?, ?)",
            session["user_id"],
            request.form.get("name"),
            f.encrypt(request.form.get("password").encode())
        )

        return redirect("/")
    else:
        return redirect("/")


# ****************************** DELETE ROUTE ***************************************************

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    password = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"]
    )
    stored_hash = password[0]["password"]
    # here to change
    if f.decrypt(stored_hash).decode() == request.form.get("checkpassword"):
        db.execute("DELETE FROM passwords WHERE id = ?", id)

    return redirect("/")


# ****************************** SHOW ROUTE *******************************************************

@app.route("/show/<int:id>", methods=["POST"])
@login_required
def show(id):

    password = db.execute(
        "SELECT password FROM users WHERE id = ?", session["user_id"]
    )
    stored_hash = password[0]["password"]
    # here to change
    if f.decrypt(stored_hash).decode() == request.form.get("checkpassword"):
        new_data = db.execute(
            "SELECT id, accountname, accountpassword  FROM passwords WHERE user_id = ?",
            session["user_id"]
        )
        for row in new_data:
            row["accountpassword"] = f.decrypt(row["accountpassword"]).decode()
        return render_template("home.html", datas=new_data, selected_id=id)
    else:

        return redirect("/")


# *********************************** login route *******************************************
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("login.html", error="Username required")
        elif not request.form.get("password"):
            return render_template("login.html", error="Password required")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )
        # here change
        if len(rows) != 1 or (f.decrypt(rows[0]["password"]).decode() != request.form.get("password")):
            return render_template("login.html", error="Invalid password and Username")
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")

# *********************************** LOGOUT ROUTE **************************************************


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ************************************ REGISTER ROUTE ****************************************************
@app.route("/register", methods=["Get", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        isvalid, message = is_strong_password(request.form.get("password"))
        if not request.form.get("username"):
            return render_template("register.html", error="Username required")
        elif not request.form.get("password"):
            return render_template("register.html", error="Password required")
        elif not isvalid:
            return render_template("register.html", error=message)
        elif not request.form.get("confirmation"):
            return render_template("register.html", error="Confirm password is required")
        elif request.form.get("confirmation") != request.form.get("password"):
            return render_template("register.html", error="Password not match")
        user = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))
        if len(user) != 0:
            return render_template("register.html", error="User already exists")
            # here change
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", request.form.get("username"), f.encrypt
                   (request.form.get("password").encode()))

        user = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        session["user_id"] = user[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")
