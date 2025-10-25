from flask import Flask, render_template, request, redirect
import csv, os

app = Flask(__name__)

# Ensure data folder and file exist
DATA_FILE = os.path.join("data", "orders.csv")
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Address", "Items"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/order", methods=["POST"])
def order():
    name = request.form.get("name","")
    phone = request.form.get("phone","")
    address = request.form.get("address","")
    items = request.form.get("items","")

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, address, items])

    return redirect("/success")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
