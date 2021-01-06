from flask import Flask, render_template, request, session

@app.route("/", methods=["GET", "POST"])
def root():
    if(credentialsWork()):
        return render_template("general.html")
    return render_template("login_or_register.html")

@app.rout("/register", methods=["GET", "POST"])
def register():
    