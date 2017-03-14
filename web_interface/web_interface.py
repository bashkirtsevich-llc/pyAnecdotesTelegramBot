from flask import Flask
from flask import render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.anecdotes


@app.route("/")
def show_index():
    return render_template("index.html")


@app.route("/users")
def show_users():
    users = db.journal.distinct("user")

    return render_template("users.html", users=users)


@app.route("/messages")
def show_messages():
    messages = db.journal.distinct("text")

    return render_template("messages.html", messages=messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
