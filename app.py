#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)

# main page
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create-account")
def user():
    return "<h1>Create new account<h1>"

@app.route("/order")
def order():
    return "<h1>Order Food<h1>"

@app.route("/payment")
def payment():
    return "<h1>Pay<h1>"

@app.route("/addresses")
def addresses():
    return "<h1>Address List<h1>"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5152)
