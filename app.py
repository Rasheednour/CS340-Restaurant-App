#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)

# main page
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create-account")
def user():
    return render_template("create.html")

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/addresses")
def addresses():
    return render_template("addresses.html")

@app.route("/finish")
def finish():
    return render_template("finish.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
