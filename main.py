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
    if "id_user" in session.keys():
        return redirect(url_for("discussion_topic"))
    else:
        return redirect(url_for("Login"))


@app.route("/discussion_topic", endpoint="discussion_topic")
def discussion_topic():
    if "id_user" not in session.keys():
        return redirect(url_for("index"))
    category_list = db_scripts.get_all_category()
    all_discussion_topic = db_scripts.get_all_category_or_discussion_topic()
    return render_template("discussion_topic/discussion_topic.html", 
                           category_list=category_list, 
                           data=all_discussion_topic, 
                           id_email=session.get("email_user"),
                           id_user=session.get("id_user")
                           )



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
            print("Error while adding theme:", e)
            return render_template("404.html")

    category_list = db_scripts.get_all_category()
    return render_template("discussion_topic/discussion_topic_create.html", category_list=category_list, id_user=session.get("id_user"))


@app.route("/discussion_topic/category/<int:id_category>", endpoint="category_discussion_topic")
def category_discussion_topic(id_category: int):
    data = db_scripts.get_category_discussion_topic(id_category)
    if request.method == "POST":
        pass
    return render_template("discussion_topic/category_discussion_topic.html", data=data, 
                           id_user=session.get("id_user"))


@app.route("/discussion_topic/<int:id>", methods=["GET", "POST"], endpoint="view_discussion_topic")
def view_discussion_topic(id: int = None):
    data = db_scripts.get_discussion_topic(id)
    if request.method == "POST" and session.get("id_user"):
        if session.get("id_user") >= 1:
            current_datetime = datetime.now()
            datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            x = db_scripts.add_comment(
                id,
                session.get("id_user"),
                request.form.get("text"),
                datetime_str
            )

    creator = session.get("id_user") == data[2]
    all_comment = db_scripts.get_all_comment(id)
    return render_template(
        "discussion_topic/view_discussion_topic.html",
        creator=creator,
        data=data,
        topic_id=id,
        topic_title=data[3],
        topic_text=data[4],
        comment_list=all_comment, 
        id_user=session.get("id_user")
    )


@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        login_email = request.form.get("email")
        password = request.form.get("password")
        id_user = db_scripts.login_user(login_email, password)
        if id_user:
            session["id_user"] = id_user
            session["id_email"] = login_email
            return redirect(url_for("discussion_topic"))
        error = "Wrong pass or mail"
        return render_template("login/login.html", error=error)
    return render_template("login/login.html")

  


@app.route("/Registration", methods=["GET", "POST"], endpoint="Registration")
def Login():
    error = None
    if request.method == "POST":
        login_email = request.form.get("login")
        password1 = request.form.get("pass1")
        password2 = request.form.get("pass2")
        id_user = db_scripts.registration_user(login_email, password1, password2)
        if id_user:
            session["id_user"] = id_user
            return redirect(url_for("discussion_topic"))
        else:
            error = "Not correcr password"
    return render_template("login/Registration.html", error=error, 
                           id_user=session.get("id_user"))



@app.route("/Exit", endpoint="Exit")
def Exit():
    if "id_user" in session.keys():
        del session["id_user"]
    if "id_email" in session.keys():
        del session["id_email"]
    return redirect(url_for("index"))

@app.route("/discussion_topic/<int:topic_id>/delete_comment/<int:id_comment>", methods=["POST"])
def delete_comment(topic_id, id_comment):
    db_scripts.del_comment(id_comment)
    return redirect(f"/discussion_topic/{topic_id}")


@app.route("/discussion_topic/<int:id>/save", methods=["POST"])
def save_topic_text(id):
    new_text = request.form.get("new_text")
    db_scripts.update_discussion_text(id, new_text)
    return redirect(f"/discussion_topic/{id}")


app.run(host="0.0.0.0", port=5000)