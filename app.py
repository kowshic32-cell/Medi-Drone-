
from flask import Flask, render_template, request, redirect, session, jsonify
import random

app = Flask(__name__)
app.secret_key = "medidrone-secret"

users = {"doctor": "1234"}
drone_position = {"x": 0, "y": 0}
chat_messages = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        if user in users and users[user] == pwd:
            session["username"] = user
            return redirect("/home")
        return "<h3>Invalid credentials</h3><a href='/'>Try again</a>"
    return render_template("login.html")

@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/")
    return render_template("index.html", user=session["username"])

@app.route("/map")
def map_page():
    if "username" not in session:
        return redirect("/")
    return render_template("map.html")

@app.route("/drone_position")
def drone_position_api():
    drone_position["x"] += random.randint(-1, 1)
    drone_position["y"] += random.randint(-1, 1)
    return jsonify(drone_position)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        msg = request.form["message"]
        chat_messages.append(f"{session['username']}: {msg}")
        return redirect("/chat")
    return render_template("chat.html", messages=chat_messages)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
