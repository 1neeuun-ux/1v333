from flask import Flask, redirect, url_for, request, session, render_template
import db_scripts
import os


from dotenv import load_dotenv
path = os.getcwd()
app = Flask(__name__,
            template_folder=os.path.join(path, "v3", "templates"),
            static_folder=os.path.join(path, "v3", "static"))



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
    return render_template("discussion topic/discussion_topic.html", category_list=category_list, data=all_discussion_topic, id_user=session.get("id_user"))



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
            print("Ошибка при добавлении темы:", e)
            return render_template("404.html")

    category_list = db_scripts.get_all_category()
    return render_template("discussion topic/discussion_topic_create.html", category_list=category_list, id_user=session.get("id_user"))


@app.route("/discussion_topic/category/<int:id_category>", endpoint="category_discussion_topic")#
def category_discussion_topic(id_category: int):
    data = db_scripts.get_category_discussion_topic(id_category)
    if request.method == "POST":
        pass

    return render_template("", data=data)


@app.route("/discussion_topic/<int:id>", endpoint="view_discussion_topic")
def view_discussion_topic(id: int = None):
    data = db_scripts.get_discussion_topic(id)
    # user = db_scripts.get_user(data[2])
    # comment_list = db_scripts.get_all_comment()
    creator = session["id_user"] == data[4]
    if creator:
        if request.method == "PUT":
            pass
        elif request.method == "PATCH":
            pass
        elif request.method == "DELETE":
            pass

    return render_template(
        "",
        creator=creator,
        data=data,
        # user=user,
        topic_title=data[2],
        topic_text=data[3]
        # comment_list=comment_list
    )


app.run(host="0.0.0.0", port=443)
