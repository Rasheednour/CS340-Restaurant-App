#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'global_foods'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
# main page
@app.route("/")
def home():

    # cur = mysql.connection.cursor()
    # cur.execute('''DROP TABLE IF EXISTS example''')

    # return "done"
    return render_template("home.html")

@app.route("/foods")
def foods():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * from foods''')
    rows = cur.fetchall()
    return render_template("foods.html", rows=rows)

@app.route("/foods", methods=['POST'])
def food_form_post():
    cur = mysql.connection.cursor()
    data = request.form
    values = (data["name"], data["description"], data["category"], data["calories"], data["cuisine"], data["price"])
    sql = ('''INSERT INTO foods (foodName, foodDescription, foodCategory, calories, cuisine, price)
                VALUES (%s, %s, %s, %s, %s, %s)''')
    cur.execute(sql, values)
    mysql.connection.commit()
    return foods()

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
