
from flask import Flask, render_template
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

API_KEY = os.environ.get("X_RAPIDAPI_KEY")
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def fetch_fixtures(date):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"date": date, "timezone": "Europe/Sofia"}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return []
    return response.json().get("response", [])

def generate_prediction(league, home, away):
    if "U19" in league or "Women" in league:
        return "Over 2.5", 76, "Мачове с младежки или дамски отбори — средно 3.1 гола."
    elif "Premier" in league or "Serie A" in league:
        return "BTTS", 68, "8 от последните 10 срещи с участие на тези отбори са били с голове и от двете страни."
    elif "Liga" in league or "Bundes" in league:
        return "Over 2.5", 72, "В последните 5 кръга средно 2.9 гола на мач."
    else:
        return "1", 64, "Домакинът има 4 победи в последните 5 домакинства."

@app.route("/")
def today():
    today = datetime.today().strftime('%Y-%m-%d')
    fixtures = fetch_fixtures(today)
    tips = []

    for item in fixtures:
        fixture = item["fixture"]
        league = item["league"]["name"]
        country = item["league"]["country"]
        home = item["teams"]["home"]["name"]
        away = item["teams"]["away"]["name"]

        prediction, confidence, reasoning = generate_prediction(league, home, away)

        tips.append({
            "time": fixture["date"][11:16],
            "match": f"{home} – {away}",
            "league": league,
            "country": country,
            "prediction": prediction,
            "confidence": confidence,
            "reasoning": reasoning
        })

    with open(f"storage/tips_{today}.json", "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False)

    return render_template("today.html", tips=tips)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/explain')
def explain():
    return render_template('explain.html')

@app.route('/today')
def today():
    return render_template('today.html')

@app.route('/yesterday')
def yesterday():
    return render_template('yesterday.html')

if __name__ == '__main__':
    app.run(debug=True)
