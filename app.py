from flask import Flask, redirect, url_for, render_template, session, request
import os
import db_scripts


path = os.getcwd()

app = Flask(__name__,
            template_folder=os.path.join(path, "template"),
            static_folder=os.path.join(path, "static"))

app.config['SECRET_KEY'] = "L54?x*,:LZSx8$!Q7zsS3{g~qV9x8hD6"

def isLOgin(funk):
    def x(*args, **kwargs):
        if "id_user" in session:
            data = funk(*args, **kwargs)
            return data
        else:
            redirect(url_for("login"))
    return x

@isLOgin
@app.route("/")
def index():
    pass

@app.route("/registration", endpoint="registration")
def registration():
    session["id_user"] = 1
    return "You registraited"
    

@app.route("/login", endpoint="login")
def registration():
    session["is_user"] = 1
    return "You entered"
    
@app.route("/login", endpoint="logout")
def logout():
    del session["id_user"]
    return redirect(url_for("login"))