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

    # db_instance= mysql.connection.cursor()
    # db_instance.execute('''DROP TABLE IF EXISTS example''')

    # return "done"
    return render_template("home.html")


# listing the restrant database
# this function needs to be broken into two functions, first a function that reads arguments and pass them to second function
# second function then performs actions shown in the bottom in if() statements.
@app.route("/restauarant-database", methods=['POST', 'GET'])
def process_request():
    food_search = ()
    link = "restaurant-database.html"

    if request.method == 'POST':
        db_instance = mysql.connection.cursor()
        data = request.form
        
        # check if it's a search post method
        if 'insert-food-form' in data:
            values = (data["name"], data["description"], data["category"], data["calories"], data["cuisine"], data["price"])
            query = ('''INSERT INTO foods (foodName, foodDescription, foodCategory, calories, cuisine, price)
                    VALUES (%s, %s, %s, %s, %s, %s)''')
            db_instance.execute(query, values)
            mysql.connection.commit()

        elif 'search-form' in data:
            query= (''' SELECT * FROM foods WHERE foodName = (%s) ''')
            search = data["search"]
            db_instance.execute(sql, [search])
            search_result = db_instance.fetchall()
            food_search = search_result

        elif 'insert-order-form' in data:
            values = (data["customerID"], data["orderProgress"], data["totalPrice"], data["orderDate"])
            query= ('''INSERT INTO orders (customerID, orderProgress, totalPrice, orderDate)
                    VALUES (%s, %s, %s, %s)''')
            db_instance.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/orders.html"

        elif 'insert-items-form' in data:
            values = (data["orderID"], data["foodID"], data["quantity"], data["totalPrice"])
            query= ('''INSERT INTO orderitems (orderID, foodID, quantity, totalPrice)
                    VALUES (%s, %s, %s, %s)''')
            db_instance.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/items.html"

        elif 'insert-payments-form' in data:
            values = (data["customerID"], data["orderID"], data["paymentDate"], data["paymentAmount"], data["paymentMethod"])
            query= ('''INSERT INTO payments (customerID, orderID, paymentDate, paymentAmount, paymentMethod)
                    VALUES (%s, %s, %s, %s, %s)''')
            db_instance.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/payments.html"

        elif 'insert-customers-form' in data:
            values = (data["firstName"], data["lastName"], data["email"], data["phoneNumber"])
            query= ('''INSERT INTO customers (firstName, lastName, email, phoneNumber)
                    VALUES (%s, %s, %s, %s)''')
            db_instance.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/customers.html"

        elif 'insert-addresses-form' in data:
            values = (data["city"], data["streetName"], data["streetNumber"])
            query= ('''INSERT INTO addresses (city, streetName, streetNumber)
                    VALUES (%s, %s, %s)''')
            db_instance.execute(sql, values)
            mysql.connection.commit()
            link = "/pages/addresses.html"

        elif 'delete' in data:
            return rem_item(request.form)

    
    return get_items()

# get database items
def get_items():
    food_search = ()
    link = "restaurant-database.html"

    db_instance= mysql.connection.cursor()

    db_instance.execute('''SELECT * from foods''')
    foods = db_instance.fetchall()
    db_instance.execute('''SELECT * from orders''')
    orders = db_instance.fetchall()

    db_instance.execute('''SELECT * from orderItems''')
    order_items = db_instance.fetchall()

    db_instance.execute('''SELECT * from customers''')
    customers = db_instance.fetchall()

    db_instance.execute('''SELECT * from addresses''')
    addresses = db_instance.fetchall()

    db_instance.execute('''SELECT * from payments''')
    payments = db_instance.fetchall()

    return render_template(link, foods=foods, orders=orders, 
                          order_items=order_items, customers=customers, 
                          addresses=addresses, payments=payments, 
                          food_search=food_search)


# remove an item 
@app.route("/restauarant-database", methods=['POST'])
def rem_item(param):

    table = param['table']   # type of table to delete from
    idType = param['idType'] # type of id to delete
    delID = param[idType]    # actual id to delete
    

    enab = "SET FOREIGN_KEY_CHECKS=0"

    print(param)

    query = "DELETE FROM " + table + " WHERE " + idType + " = " + delID
    
    db_instance= mysql.connection.cursor()
    
    db_instance.execute(enab)
    db_instance.execute(query)

    mysql.connection.commit()

    return get_items() 

if __name__ == "__main__":

    # starting flask listening socket
    app.run(host='0.0.0.0', debug=True, port=5000)
