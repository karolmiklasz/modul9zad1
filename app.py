import requests
import csv
from flask import Flask, render_template, request

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()


rates = data[0]["rates"]

csv_filename = "exchange_rates.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["currency", "code", "bid", "ask"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()

    for rate in rates:
        writer.writerow(rate)

def calculate_cost(currency_code, amount):
    for rate in rates:
        if rate["code"] == currency_code:
            exchange_rate = rate["ask"]
            cost_in_pln = amount * exchange_rate
            return cost_in_pln

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        currency_code = request.form["currency"]
        amount = float(request.form["amount"])
        cost_in_pln = calculate_cost(currency_code, amount)
        return render_template("index.html", rates=rates, cost_in_pln=cost_in_pln)
    else:
        return render_template("index.html", rates=rates, cost_in_pln=None)

if __name__ == "__main__":
    app.run(debug=True)