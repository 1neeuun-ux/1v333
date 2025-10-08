from flask import Flask, redirect, url_for, request, session, render_template
import db_scripts
from datetime import datetime
import os


from dotenv import load_dotenv
path = os.getcwd()

app = Flask(__name__,
            template_folder=os.path.join("v3", "templates"),
            static_folder=os.path.join("v3", "static"))

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/", endpoint="index", methods=["GET"])
def index():
    return redirect(url_for("discussion_topic"))

@app.route("/discussion_topic", endpoint="discussion_topic")
def discussion_topic():
    category_list = db_scripts.get_all_category()
    all_discussion_topic = db_scripts.get_all_category_or_discussion_topic()
    print()
    return render_template("discussion_topic/discussion_topic.html", 
                           category_list=category_list, 
                           data=all_discussion_topic, 
                           id_user=session.get("id_user"))



@app.route("/discussion_topic/create", methods=["GET", "POST"], endpoint="discussion_topic_create")
def discussion_topic_create():
    if request.method == "POST":
        try:
            id_category = int(request.form.get("id_category"))
            id_user = session.get("id_user")
            title = request.form.get("title")
            text = request.form.get("text")

            if db_scripts.add_discussion_topic(id_category, id_user, title, text):
                return redirect(url_for("index"))
            else:
                return render_template("404.html")
        except Exception as e:
            print("Error whil adding theme:", e)
            return render_template("404.html")

    category_list = db_scripts.get_all_category()
    return render_template("discussion_topic/discussion_topic_create.html", category_list=category_list, id_user=session.get("id_user"))


@app.route("/discussion_topic/category/<int:id_category>", endpoint="category_discussion_topic")
def category_discussion_topic(id_category: int):
    data = db_scripts.get_category_discussion_topic(id_category)
    if request.method == "POST":
        pass
    return render_template("discussion_topic/category_discussion_topic.html", data=data)


@app.route("/discussion_topic/<int:id>", methods=["GET", "POST"], endpoint="view_discussion_topic")
def view_discussion_topic(id: int = None):
    data = db_scripts.get_discussion_topic(id)
    
    creator = session.get("id_user") == data[2]
    all_comment = db_scripts.get_all_comment(id)
    
    session["id_user"] = 1
    if request.method == "POST" and session.get("id_user"):
        if session.get("id_user") >= 1:
            current_datetime = datetime.now()
            datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            x = db_scripts.add_comment_(id,
                                    session.get("text"),
                                    str(request.form.get("text")),
                                    datetime_str)
            print(x)

    if creator:
        if request.method == "PUT":
            pass
        elif request.method == "PATCH":
            pass
        elif request.method == "DELETE":
            pass

    return render_template(
        "discussion_topic/view_discussion_topic.html",
        creator=creator,
        data=data,
        topic_title=data[3],
        topic_text=data[4],
        all_comment = all_comment
    )


@app.route("/Login_user", methods=["GET", "POST"], endpoint="Login")
def Login():
    login = request.form.get("login")
    password = request.form.get("pass")
    id = db_scripts.login_user(login, password)
    if id:
        session["id_user"] = id
        return redirect(url_for("discussion_topic"))
    return render_template("login/login.html")    
    
@app.route("/Registration_user", methods=["GET", "POST"], endpoint="Registration")
def Registration():
    login = request.form.get("login")
    password1 = request.form.get("pass1")
    password2 = request.form.get("pass2")
    id = db_scripts.registration_user(login, password1, password2)
    if id:
        session["id_user"] = id
        return redirect(url_for("discussion_topic"))
    return render_template("login/Registration.html")   

@app.route("/Exit", endpoint="Exit")
def Exit():
    del session["id_user"]
    session["id_user"] = -1
    return redirect(url_for("discussion_topic"))

app.run(host="0.0.0.0", port=5000)
