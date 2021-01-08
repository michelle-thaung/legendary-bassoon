from flask import Flask, render_template, request, session
import os
from database import Database
from middleware import protected

app = Flask(__name__)
db = Database("fruit_for_blogs.db")

@app.route("/", methods=["GET", "POST"])
@protected(signed_in=True, goto="/home")
def root():
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
@protected(signed_in=True, goto="/home")
def login():
    if(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        if(username == "" or password == ""):
            return render_template("login.html", error="Please fill in your credentials")
        elif(not(db.check_credentials(username, password))):
            return render_template("login.html", error="Wrong credentials!")
        else:
            session["username"] = username
            session["password"] = password
    if("username" in session and "password" in session and db.check_credentials(session["username"], session["password"])):
        return render_template("home.html", collection=db.get_all_blogs(), user_collection=db.get_all_users())
    return render_template("login.html", error="")

@app.route("/home", methods=["GET"])
@protected(signed_in=False, goto="/")
def home():
    return render_template("home.html", collection=db.get_all_blogs(), user_collection=db.get_all_users())

@app.route("/logout", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
def logout():
    if(request.method == "POST"):
        session.pop("username")
        session.pop("password")
    return render_template("login_or_register.html")

@app.route("/edit", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
def edit():
    return render_template("edit_blogs.html", collection=db.get_blogs(session["username"]))

@app.route("/user-blog", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
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

@app.route("/new-entry", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
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

@app.route("/input-entry", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
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

@app.route("/new-blog", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
def new_blog():
    if(request.method == "POST"):
        blog_name = request.form["blog_name"]
        description = request.form["description"]
        if(blog_name == "" or description == ""):
            return render_template("new_blog.html", error="Please fill in all of the boxes below:")
        db.insert_blog(session["username"], blog_name, description)
        return render_template("home.html", collection=db.get_all_blogs(), user_collection=db.get_all_users())
    return render_template("new_blog.html", error="")

@app.route("/view-blog", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
def view_blog():
    info = db.get_blog(request.form["blog"])
    webpage = "other_blog.html"
    return render_template(webpage, 
        blog_name=info["title"], 
        update=info["time"], 
        description=info["description"], 
        blog_author=info["author"], 
        collection=info["entries"],
        id=info["id"]
    )

@app.route("/edit-blog", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
def edit_blog():
    db.update_blog(request.form["blog"], request.form["title"], request.form["description"])
    info = db.get_blog(request.form["blog"])
    return render_template("user_blog.html", 
        blog_name=info["title"], 
        update=info["time"], 
        description=info["description"], 
        blog_author=info["author"], 
        collection=info["entries"],
        id=info["id"]
    )

@app.route("/edit-entry", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
def edit_entry():
    db.update_entry(request.form["entryID"], request.form["body"])
    info = db.get_blog(request.form["blog"])
    return render_template("user_blog.html", 
        blog_name=info["title"], 
        update=info["time"], 
        description=info["description"], 
        blog_author=info["author"], 
        collection=info["entries"],
        id=info["id"]
    )

@app.route("/view-user", methods=["GET", "POST"])
@protected(signed_in=False, goto="/")
def view_user():
    username = request.form["user"]
    if(request.form["user"] == session["username"]):
        username = "Your"
    return render_template("view_blogs.html", user=username, collection=db.get_blogs(request.form["user"]))

if(__name__ == "__main__"):
    app.secret_key = os.urandom(32)
    app.debug = False
    app.run()