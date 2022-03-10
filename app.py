#!/usr/bin/env python3
from audioop import add
from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL


# initializing flask
app = Flask(__name__)

# database settings
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'global_foods'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# initializnig mysql object
mysql = MySQL(app)

# json carrying food options


# main page
@app.route("/")
def home():

    # cur = mysql.connection.cursor()
    # cur.execute('''DROP TABLE IF EXISTS example''')

    # return "done"
    return render_template("home.html")


# listing the restrant database
@app.route("/restauarant-database", methods=['POST', 'GET'])
def restaurant_database():
    food_search = ()
    link = "restaurant-database.html"

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        data = request.form

        if 'delete-food' in data:
            values = (data["foodID"],)
            sql = ('''DELETE FROM orderItems WHERE foodID = (%s)''')
            cur.execute(sql, values)
            sql = ('''DELETE FROM foods WHERE foodID = (%s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        if 'food-form' in data:
            values = (data["name"], data["description"], data["category"], data["calories"], data["cuisine"], data["price"])
            sql = ('''INSERT INTO foods (foodName, foodDescription, foodCategory, calories, cuisine, price)
                    VALUES (%s, %s, %s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'search-form' in data:
            sql = (''' SELECT * FROM foods WHERE foodName = (%s) ''')
            search = data["search"]
            cur.execute(sql, [search])
            search_result = cur.fetchall()
            food_search = search_result

        elif 'order-form' in data:
            values = (data["customerID"], data["orderProgress"], data["totalPrice"], data["orderDate"])
            sql = ('''INSERT INTO orders (customerID, orderProgress, totalPrice, orderDate)
                    VALUES (%s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/orders.html"

        elif 'items-form' in data:
            values = (data["orderID"], data["foodID"], data["quantity"], data["totalPrice"])
            sql = ('''INSERT INTO orderitems (orderID, foodID, quantity, totalPrice)
                    VALUES (%s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/items.html"

        elif 'payments-form' in data:
            values = (data["customerID"], data["orderID"], data["paymentDate"], data["paymentAmount"], data["paymentMethod"])
            sql = ('''INSERT INTO payments (customerID, orderID, paymentDate, paymentAmount, paymentMethod)
                    VALUES (%s, %s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/payments.html"

        elif 'customers-form' in data:
            values = (data["firstName"], data["lastName"], data["email"], data["phoneNumber"])
            sql = ('''INSERT INTO customers (firstName, lastName, email, phoneNumber)
                    VALUES (%s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/customers.html"

        elif 'addresses-form' in data:
            values = (data["city"], data["streetName"], data["streetNumber"])
            sql = ('''INSERT INTO addresses (city, streetName, streetNumber)
                    VALUES (%s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/addresses.html"

    print("food search is", food_search)
    cur = mysql.connection.cursor()

    cur.execute('''SELECT * from foods''')
    foods = cur.fetchall()
    cur.execute('''SELECT * from orders''')
    orders = cur.fetchall()

    cur.execute('''SELECT * from orderItems''')
    order_items = cur.fetchall()

    cur.execute('''SELECT * from customers''')
    customers = cur.fetchall()

    cur.execute('''SELECT * from addresses''')
    addresses = cur.fetchall()

    cur.execute('''SELECT * from payments''')
    payments = cur.fetchall()

    return render_template(link, foods=foods, orders=orders, 
                                     order_items=order_items, customers=customers, 
                                           addresses=addresses, payments=payments, 
                                     food_search=food_search)


@app.route("/restauarant-database", methods=['DELETE'])
def delete_row():
    
    cur = mysql.connection.cursor()
    data = request.form
    print("did i get here?")

    if 'delete-food' in data:
        values = (data["delete-food"])
        print("values are: ", values)
        # sql = ('''DELETE FROM foods WHERE foodID = (%s)''')
        # cur.execute(sql, values)
        # mysql.connection.commit()
        restaurant_database()

    elif 'delete-order' in data:
        values = (data["customerID"], data["orderProgress"], data["totalPrice"], data["orderDate"])
        sql = ('''DELETE FROM orders (customerID, orderProgress, totalPrice, orderDate)
                VALUES (%s, %s, %s, %s)''')
        cur.execute(sql, values)
        mysql.connection.commit()
        restaurant_database()

    elif 'delete-item' in data:
        values = (data["orderID"], data["foodID"], data["quantity"], data["totalPrice"])
        sql = ('''DELETE FROM orderitems (orderID, foodID, quantity, totalPrice)
                VALUES (%s, %s, %s, %s)''')
        cur.execute(sql, values)
        mysql.connection.commit()
        restaurant_database()

    elif 'delete-payment' in data:
        values = (data["customerID"], data["orderID"], data["paymentDate"], data["paymentAmount"], data["paymentMethod"])
        sql = ('''DELETE FROM payments (customerID, orderID, paymentDate, paymentAmount, paymentMethod)
                VALUES (%s, %s, %s, %s, %s)''')
        cur.execute(sql, values)
        mysql.connection.commit()
        restaurant_database()

    elif 'delete-customer' in data:
        values = (data["firstName"], data["lastName"], data["email"], data["phoneNumber"])
        sql = ('''DELETE FROM customers (firstName, lastName, email, phoneNumber)
                VALUES (%s, %s, %s, %s)''')
        cur.execute(sql, values)
        mysql.connection.commit()
        restaurant_database()

    elif 'delete-address' in data:
        values = (data["city"], data["streetName"], data["streetNumber"])
        sql = ('''DELETE FROM addresses (city, streetName, streetNumber)
                VALUES (%s, %s, %s)''')
        cur.execute(sql, values)
        mysql.connection.commit()
        restaurant_database()





if __name__ == "__main__":

    # starting flask listening socket
    app.run(host='0.0.0.0', debug=True, port=5000)
