#!/usr/bin/env python3
from flask import Flask 

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Restaurant Home Page<h1>"

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
    app.run(host='0.0.0.0', port=5152)
