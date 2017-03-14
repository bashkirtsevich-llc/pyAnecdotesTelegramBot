from flask import Flask
from flask import render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.anecdotes


@app.route('/')
def show_index():
    return render_template("index.html")


@app.route('/users')
def show_users():
    users = db.journal.distinct("user")

    users_list = u"\r\n".join(
        map(lambda e: u"id: {0}\tusername: {1}\t\tfirst_name: {2}\t\tlast_name: {3}\r\n".format(
            str(e["id"]), e["username"], e["first_name"], e["last_name"]), users)
    )

    return render_template("users.html", users=users_list)


@app.route('/messages')
def show_messages():
    messages = db.journal.distinct("text")

    messages_list = u"\r\n".join(messages)

    return render_template("messages.html", messages=messages_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
