#!/usr/bin/env python3
from audioop import add
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

@app.route("/restauarant-database")
def restaurant_database():

    cur = mysql.connection.cursor()

    cur.execute('''SELECT * from foods''')
    foods = cur.fetchall()

    cur.execute('''SELECT * from orders''')
    orders = cur.fetchall()

    cur.execute('''SELECT * from orderitems''')
    order_items = cur.fetchall()

    cur.execute('''SELECT * from customers''')
    customers = cur.fetchall()

    cur.execute('''SELECT * from addresses''')
    addresses = cur.fetchall()

    cur.execute('''SELECT * from payments''')
    payments = cur.fetchall()

    return render_template("restaurant-database.html", foods=foods, orders=orders, order_items=order_items, customers=customers, addresses=addresses, payments=payments)

@app.route("/restauarant-database", methods=['POST'])
def database_post():
    cur = mysql.connection.cursor()
    data = request.form
    values = (data["name"], data["description"], data["category"], data["calories"], data["cuisine"], data["price"])
    sql = ('''INSERT INTO foods (foodName, foodDescription, foodCategory, calories, cuisine, price)
              VALUES (%s, %s, %s, %s, %s, %s)''')
    cur.execute(sql, values)
    mysql.connection.commit()
    return restaurant_database()

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
