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
            sql = ('''DELETE FROM OrderItems WHERE foodID = (%s)''')
            cur.execute(sql, values)
            sql = ('''DELETE FROM Foods WHERE foodID = (%s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'delete-order' in data:
            values = (data["orderID"],)
            sql = ('''DELETE FROM OrderItems WHERE orderID = (%s)''')
            cur.execute(sql, values)
            sql = ('''DELETE FROM Payments WHERE orderID = (%s)''')
            cur.execute(sql, values)
            sql = ('''DELETE FROM Orders WHERE orderID = (%s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'delete-item' in data:
            values = (data["orderID"],)
            sql = ('''DELETE FROM OrderItems WHERE orderID = (%s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'delete-payment' in data:
            values = (data["paymentID"],)
            sql = ('''DELETE FROM Payments WHERE paymentID = (%s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'delete-customer' in data:
            values = (data["customerID"],)
            sql = ('''DELETE FROM Addresses WHERE customerID = (%s)''')
            cur.execute(sql, values)
            sql = ('''DELETE FROM Customers WHERE customerID = (%s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'delete-address' in data:
            values = (data["addressID"],)
            sql = ('''DELETE FROM Addresses WHERE addressID = (%s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'food-form' in data:
            values = (data["name"], data["description"], data["category"], data["calories"], data["cuisine"], data["price"])
            sql = ('''INSERT INTO Foods (foodName, foodDescription, foodCategory, calories, cuisine, price)
                    VALUES (%s, %s, %s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'search-form' in data:
            sql = (''' SELECT * FROM Foods WHERE foodName = (%s) ''')
            search = data["search"]
            cur.execute(sql, [search])
            search_result = cur.fetchall()
            food_search = search_result

        elif 'order-form' in data:
            values = (data["customerID"], data["orderProgress"], data["orderDate"])
            sql = ('''INSERT INTO Orders (customerID, orderProgress, orderDate)
                    VALUES (%s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            # link = "/pages/orders.html"

        elif 'items-form' in data:
            
            id = (data["foodID"],)
            sql = ('''SELECT price FROM Foods WHERE foodID = (%s)''')
            cur.execute(sql, id)
            result = cur.fetchall()
            quantity = float(data["quantity"])
            total = result[0]["price"] * quantity

            values = (data["orderID"], data["foodID"], data["quantity"], total)

            sql = ('''INSERT INTO OrderItems (orderID, foodID, quantity, totalPrice)
                    VALUES (%s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            # link = "/pages/items.html"

        elif 'payments-form' in data:
            values = (data["customerID"], data["orderID"], data["paymentDate"], data["paymentAmount"], data["paymentMethod"])
            sql = ('''INSERT INTO Payments (customerID, orderID, paymentDate, paymentAmount, paymentMethod)
                    VALUES (%s, %s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            # link = "/pages/payments.html"

        elif 'customers-form' in data:
            values = (data["firstName"], data["lastName"], data["email"], data["phoneNumber"])
            sql = ('''INSERT INTO Customers (firstName, lastName, email, phoneNumber)
                    VALUES (%s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            # link = "/pages/customers.html"

        elif 'addresses-form' in data:
            values = (data["city"], data["streetName"], data["streetNumber"])
            sql = ('''INSERT INTO Addresses (city, streetName, streetNumber)
                    VALUES (%s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            # link = "/pages/addresses.html"

    cur = mysql.connection.cursor()

    cur.execute('''SELECT * from Foods''')
    foods = cur.fetchall()
    cur.execute('''SELECT * from Orders''')
    orders = cur.fetchall()

    cur.execute('''SELECT * from OrderItems''')
    order_items = cur.fetchall()

    cur.execute('''SELECT * from Customers''')
    customers = cur.fetchall()

    cur.execute('''SELECT * from Addresses''')
    addresses = cur.fetchall()

    cur.execute('''SELECT * from Payments''')
    payments = cur.fetchall()

    return render_template(link, foods=foods, orders=orders, 
                                     order_items=order_items, customers=customers, 
                                           addresses=addresses, payments=payments, 
                                     food_search=food_search)



if __name__ == "__main__":

    # starting flask listening socket
    app.run(host='0.0.0.0', debug=True, port=5000)
