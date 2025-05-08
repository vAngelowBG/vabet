from flask import Flask, render_template
import os

os.makedirs("storage", exist_ok=True)

app = Flask(__name__)

@app.route("/today")
def today():
    # Примерен списък с мачове и прогнози
    matches = [
        {"match": "Барселона – Реал Мадрид", "prediction": "Over 2.5", "confidence": 78, "reason": "Двата отбора вкарват често"},
        {"match": "Байерн – Борусия Д", "prediction": "BTTS", "confidence": 72, "reason": "И двата имат силна атака"},
        {"match": "Ливърпул – Челси", "prediction": "1", "confidence": 66, "reason": "Ливърпул е непобеден у дома"}
    ]
    return render_template("today.html", matches=matches)
    
if __name__ == "__main__":
    app.run(debug=True)