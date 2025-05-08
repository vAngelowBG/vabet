
from flask import Flask, render_template, jsonify
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
        matches.append({
            "time": fixture["date"][11:16],
            "match": f"{teams['home']['name']} – {teams['away']['name']}",
            "league": league["name"],
            "country": league["country"]
        })
    return matches


@app.route("/")
def home():
    matches = get_today_matches()
    return render_template("today.html", matches=matches)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
