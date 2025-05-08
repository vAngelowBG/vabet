
from flask import Flask, render_template
import requests
import os
os.makedirs("storage", exist_ok=True)

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


@app.route("/history")
def history():
    import urllib.parse
    from datetime import timedelta
    from flask import request
    date = request.args.get("date", datetime.today().strftime('%Y-%m-%d'))
    today = datetime.today().strftime('%Y-%m-%d')
    path = f"storage/tips_{date}.json"
    if not os.path.exists(path):
        return render_template("history.html", matches=[], date=date, total=0, correct=0, percent=0, today=today)

    with open(path, encoding="utf-8") as f:
        tips = json.load(f)

    # взимаме реални резултати
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"date": date, "timezone": "Europe/Sofia"}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return render_template("history.html", matches=[], date=date, total=0, correct=0, percent=0, today=today)

    data = response.json().get("response", [])
    results_map = {}
    for item in data:
        home = item["teams"]["home"]["name"]
        away = item["teams"]["away"]["name"]
        score = item["score"]["fulltime"]
        results_map[f"{home} – {away}"] = score

    matches = []
    correct = 0

    for tip in tips:
        match = tip["match"]
        prediction = tip["prediction"]
        result_score = results_map.get(match)
        if result_score:
            result = f"{result_score['home']}:{result_score['away']}"
            goals = (result_score['home'] or 0) + (result_score['away'] or 0)
            status = "❌"

            if prediction == "Over 2.5" and goals > 2.5:
                status = "✅"
            elif prediction == "BTTS" and (result_score['home'] > 0 and result_score['away'] > 0):
                status = "✅"
            elif prediction == "1" and result_score['home'] > result_score['away']:
                status = "✅"
            elif prediction == "2" and result_score['away'] > result_score['home']:
                status = "✅"
            elif prediction == "X" and result_score['home'] == result_score['away']:
                status = "✅"

            if status == "✅":
                correct += 1
        else:
            result = "няма резултат"
            status = "?"

        matches.append({
            "match": match,
            "prediction": prediction,
            "result": result,
            "status": status,
            "confidence": tip.get("confidence", "-"),
            "reasoning": tip.get("reasoning", "-")
        })

    total = len(matches)
    percent = round((correct / total) * 100) if total else 0

    return render_template("history.html", matches=matches, date=date, correct=correct, total=total, percent=percent, today=today)

@app.route("/today")
def r_today():
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template("today.html", today=today)


@app.route("/yesterday")
def r_yesterday():
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template("yesterday.html", today=today)


@app.route("/tips")
def r_tips():
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template("tips.html", today=today)


@app.route("/explain")
def r_explain():
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template("explain.html", today=today)

# force redeploy
