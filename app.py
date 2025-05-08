import os
from flask import Flask, render_template

os.makedirs("storage", exist_ok=True)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/today")
def today():
    return render_template("today.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/tips")
def tips():
    return render_template("tips.html")

@app.route("/explain")
def explain():
    return render_template("explain.html")

@app.route("/yesterday")
def yesterday():
    return render_template("yesterday.html")

if __name__ == "__main__":
    app.run(debug=True)
