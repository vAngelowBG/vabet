
from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

# Фалшиви прогнози за демонстрация
sample_predictions = [
    {"match": "Ливърпул – Арсенал", "time": "21:00", "prediction": "Над 2.5", "confidence": "78%", "type": "AI"},
    {"match": "Ювентус – Интер", "time": "19:00", "prediction": "1", "confidence": "65%", "type": "AI"}
]

# Фалшива статистика за вчера
sample_stats = {"total": 10, "correct": 7, "accuracy": "70%"}


@app.route("/")
def home():
    return render_template("index.html", predictions=sample_predictions)


@app.route("/yesterday")
def yesterday():
    return render_template("yesterday.html", stats=sample_stats)


@app.route("/api/today")
def api_today():
    return jsonify(sample_predictions)


@app.route("/api/yesterday")
def api_yesterday():
    return jsonify(sample_stats)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
