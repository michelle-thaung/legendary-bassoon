from flask import Flask, render_template, request, session
from db import setup, entry_exists, register_user, display, check_credentials, return_blogs, return_blog_information
import os, sqlite3

app = Flask(__name__)

setup()

@app.route("/", methods=["GET", "POST"])
def root():
    if(False):
        return render_template("general.html")
    return render_template("login_or_register.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == "POST"):
        register_username = request.form["register_username"]
        register_password = request.form["register_password"]
        confirm = request.form["confirm"]
        blog_name = request.form["blog_name"]
        description = request.form["description"]
        if(entry_exists(register_username, "users", 0)):
            return render_template("register.html", error="Username already exists!")
        elif(confirm != register_password):
            return render_template("register.html", error="Passwords should match!")
        elif(register_username == "" or register_password == "" or confirm == "" or blog_name == "" or description == ""):
            return render_template("register.html", error="Please fill in all of the boxes below:")
        elif(not register_username.isalnum()):
            return render_template("register.html", error="The username should only contain alphanumeric characters!")
        register_user(register_username, register_password, blog_name, description)
        return render_template("registration_successful.html")
    return render_template("register.html", error="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        username = session["username"] = request.form["username"]
        password = session["password"] = request.form["password"]
        if(username == "" or password == ""):
            return render_template("login.html", error="Please fill in your credentials")
        elif(not(check_credentials(session["username"], session["password"]))):
            return render_template("login.html", error="Wrong credentials!")
    if("username" in session and "password" in session and check_credentials(session["username"], session["password"])):
        return render_template("general.html")
    return render_template("login.html", error="")

@app.route("/general", methods=["GET"])
def general():
    return render_template("general.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if(request.method == "POST"):
        session.pop("username")
        session.pop("password")
    return render_template("login_or_register.html")

@app.route("/edit", methods=["POST"])
def edit():
    return render_template("edit_blogs.html", collection=return_blogs(session["username"]))

@app.route("/user_blog", methods=["POST"])
def user_blog():
    info = return_blog_information(session["username"] + "_" + request.form["blog"])
    return render_template("user_blog.html", blog_name=info[0], update=info[2], description=info[1], collection=info[3:])

@app.route("/user", methods=["GET"])
def user():
    return render_template("user.html", collection=display("users"))

@app.route("/blog", methods=["GET"])
def blog():
    return render_template("blog.html", collection=display("blogs"))

if(__name__ == "__main__"):
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()