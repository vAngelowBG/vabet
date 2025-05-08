from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/today")
def today():
    return render_template("today.html")

@app.route("/yesterday")
def yesterday():
    return render_template("yesterday.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/explain")
def explain():
    return render_template("explain.html")

@app.route("/tips")
def tips():
    return render_template("tips.html")

if __name__ == "__main__":
    app.run(debug=True)

# redeploy trigger
