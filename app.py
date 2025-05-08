
from flask import Flask, render_template
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.environ.get("X_RAPIDAPI_KEY")
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def get_today_matches():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    today = datetime.today().strftime('%Y-%m-%d')
    params = {"date": today, "timezone": "Europe/Sofia"}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        return []

    data = response.json().get("response", [])
    matches = []
    for item in data:
        fixture = item["fixture"]
        teams = item["teams"]
        league = item["league"]

        # Mock данни за примерна логика
        home_name = teams["home"]["name"]
        away_name = teams["away"]["name"]

        # Примерна логика за прогноза
        if "U19" in league["name"] or "Women" in league["name"]:
            prediction = "Over 2.5"
            reason = "Мач с юношески или дамски отбори – обикновено резултатни."
        elif "Premier" in league["name"] or "Serie A" in league["name"]:
            prediction = "BTTS"
            reason = "Сериозни отбори с добра атака – вероятно и двата ще отбележат."
        else:
            prediction = "1X"
            reason = "Домакинът има леко предимство или по-силна форма."

        matches.append({
            "time": fixture["date"][11:16],
            "match": f"{home_name} – {away_name}",
            "league": league["name"],
            "country": league["country"],
            "prediction": prediction,
            "reason": reason
        })
    return matches

@app.route("/")
def home():
    matches = get_today_matches()
    return render_template("tips.html", matches=matches)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
