#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)

# main page
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/restaurant-database")
def restaurant_database():
    return render_template("restaurant_database.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
