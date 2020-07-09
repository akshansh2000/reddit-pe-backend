from flask import Flask, render_template, request, Response
import requests
import random
import string
import time

app = Flask(__name__)


@app.route("/")
def landing_page():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def export():
    username = request.form["reddit_username"]
    api_link = f"http://www.reddit.com/user/{username}/comments/.json"

    random_user_agent = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=16,
        )
    )
    headers = {"User-agent": random_user_agent}

    result = requests.get(api_link, headers=headers).json()["data"]["children"]
    return_string = "\n\n=============\n\n".join([
        child["data"]["body"] + "\n\n" + "Date Posted: " + time.strftime(
            "%d-%m-%Y %H:%M:%S",
            time.gmtime(child["data"]["created"]),
        ) + "\nSubReddit: " + "r/" + child["data"]["subreddit"] for child in result
    ])

    return Response(
        return_string,
        mimetype="text/plain",
        headers={"Content-disposition": f"attachment; filename={username}.txt"}
    )
