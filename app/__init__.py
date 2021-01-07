from flask import Flask, render_template, request, session
import os
from database import Database

app = Flask(__name__)
db = Database("fruit_for_blogs.db")

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
        if(db.has_username(register_username)):
            return render_template("register.html", error="Username already exists!")
        elif(confirm != register_password):
            return render_template("register.html", error="Passwords should match!")
        elif(register_username == "" or register_password == "" or confirm == "" or blog_name == "" or description == ""):
            return render_template("register.html", error="Please fill in all of the boxes below:")
        elif(not register_username.isalnum()):
            return render_template("register.html", error="The username should only contain alphanumeric characters!")
        db.register_user(register_username, register_password, blog_name, description)
        return render_template("registration_successful.html")
    return render_template("register.html", error="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        username = session["username"] = request.form["username"]
        password = session["password"] = request.form["password"]

        if(username == "" or password == ""):
            return render_template("login.html", error="Please fill in your credentials")
        elif(not(db.check_credentials(session["username"], session["password"]))):
            return render_template("login.html", error="Wrong credentials!")
    if("username" in session and "password" in session and db.check_credentials(session["username"], session["password"])):
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
    return render_template("edit_blogs.html", collection=db.get_blogs(session["username"]))

@app.route("/user_blog", methods=["POST"])
def user_blog():
    info = db.get_blog(request.form["blog"])
    return render_template("user_blog.html", 
        blog_name=info["title"], 
        update=info["time"], 
        description=info["description"], 
        blog_author=info["author"], 
        collection=info["entries"],
        id=info["id"]
    )

@app.route("/new_entry", methods=["POST"])
def new_entry():
    info = db.get_blog(request.form["blog"])
    return render_template("new_entry.html", 
        blog_name=info["title"], 
        update=info["time"], 
        description=info["description"], 
        blog_author=info["author"], 
        collection=info["entries"],
        id=info["id"]
    )

@app.route("/input_entry", methods=["POST"])
def input_entry():
    db.insert_entry(request.form["body"], request.form["blog"])
    info = db.get_blog(request.form["blog"])
    return render_template("user_blog.html",
        blog_name=info["title"], 
        update=info["time"], 
        description=info["description"], 
        blog_author=info["author"], 
        collection=info["entries"],
        id=info["id"]
    )

@app.route("/user", methods=["GET"])
def user():
    return render_template("user.html", collection=db.display("users"))

@app.route("/blog", methods=["GET"])
def blog():
    return render_template("blog.html", collection=db.display("blogs"))

if(__name__ == "__main__"):
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()