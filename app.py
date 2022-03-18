#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, redirect, url_for
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

    # detect POST methods from HTML forms which include DELETE methods as well
    if request.method == 'POST':

        # start a mysql connection
        cur = mysql.connection.cursor()

        # obtain the form data received from the request
        data = request.form

        if 'edit-food' in data:
            cur.execute('''SELECT * from Foods WHERE foodID = (%s)''', (data["foodID"], ))
            result = cur.fetchall()
            food_data = result[0]
            return render_template("./pages/edit-food.html", food_data=food_data)
        
        elif 'edit-order' in data:
            cur.execute('''SELECT * from Orders WHERE orderID = (%s)''', (data["orderID"], ))
            result = cur.fetchall()
            order_data = result[0]
            return render_template("./pages/edit-order.html", order_data=order_data)

        elif 'edit-item' in data:
            cur.execute('''SELECT * from OrderItems WHERE orderID = (%s) AND foodID = (%s) AND quantity = (%s)''', (data["orderID"], data["foodID"], data["quantity"]))
            result = cur.fetchall()
            item_data = result[0]
            return render_template("./pages/edit-item.html", item_data=item_data)

        elif 'edit-customer' in data:
            cur.execute('''SELECT * from Customers WHERE customerID = (%s)''', (data["customerID"], ))
            result = cur.fetchall()
            customer_data = result[0]

            cur.execute(''' SELECT * from Addresses WHERE customerID = (%s) ''', (data["customerID"], ))
            address_data = cur.fetchall()

            return render_template("./pages/edit-customer.html", customer_data=customer_data, address_data = address_data)

        elif 'edit-address' in data:
            cur.execute('''SELECT * from Addresses WHERE addressID = (%s)''', (data["addressID"], ))
            result = cur.fetchall()
            address_data = result[0]
            return render_template("./pages/edit-address.html", address_data=address_data)

        # for DELETE requests, detect which table requested a delete.
        elif 'delete-food' in data:
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
            values = (data["orderID"], data["foodID"], data["quantity"])

            sql = ('''SELECT totalPrice FROM orderItems WHERE orderID = (%s) AND foodID = (%s) AND quantity = (%s)''')
            
            cur.execute(sql, values)
            result = cur.fetchall()
            amount = result[0]["totalPrice"]

            sql = (''' UPDATE Orders SET totalPrice = totalPrice - (%s) WHERE orderID = (%s) ''')
            cur.execute(sql, (amount, data["orderID"]))

            sql = ('''DELETE FROM OrderItems WHERE orderID = (%s) AND foodID = (%s) AND quantity = (%s)''')
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
            
            sql = ('''SELECT * FROM Customers WHERE currentAddress = (%s)''')
            values = (data["addressID"],)
            cur.execute(sql, values)
            result = cur.fetchall()
            print("DATA IS ", data)
            if result:
                cur.execute(''' UPDATE Customers SET currentAddress = NULL WHERE customerID = (%s)''', (data["customerID"], ))

            mysql.connection.commit()


        # for INSERT requests, detect which table requested the INSERT
        elif 'food-form' in data:
            values = (data["name"], data["description"], data["category"], data["calories"], data["cuisine"], data["price"])
            sql = ('''INSERT INTO Foods (foodName, foodDescription, foodCategory, calories, cuisine, price)
                    VALUES (%s, %s, %s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()

        elif 'search-form' in data:
            sql = (''' SELECT * FROM Foods WHERE foodName LIKE (%s) ''')
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

            # update order total price
            order_id = data["orderID"]
            sql = (''' UPDATE Orders SET totalPrice = (%s) + totalPrice WHERE orderID = (%s) ''')
            values = (total, order_id)
            cur.execute(sql, values)

            values = (data["orderID"], data["foodID"], data["quantity"], total)

            sql = ('''INSERT INTO OrderItems (orderID, foodID, quantity, totalPrice)
                    VALUES (%s, %s, %s, %s)''')
            cur.execute(sql, values)
            mysql.connection.commit()
            # link = "/pages/items.html"

        elif 'payments-form' in data:
            or_id = (data["orderID"],)
            sql = (''' SELECT totalPrice FROM Orders WHERE orderID = (%s) ''')
            cur.execute(sql, or_id)
            result = cur.fetchall()
            payment_amount = result[0]["totalPrice"]

            sql = (''' SELECT customerID FROM Orders WHERE orderID = (%s) ''')
            cur.execute(sql, or_id)
            result = cur.fetchall()
            customer_id = result[0]["customerID"]


            values = (customer_id, data["orderID"], data["paymentDate"], payment_amount, data["paymentMethod"])
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
            
            values = (data["customerID"], data["city"], data["streetName"], data["streetNumber"])
            sql = ('''INSERT INTO Addresses (customerID, city, streetName, streetNumber)
                    VALUES (%s, %s, %s, %s)''')
            cur.execute(sql, values)

            customer_id = (data["customerID"],)

            sql = ('''SELECT max(addressID) as addressID FROM Addresses WHERE addressID IN (SELECT addressID FROM Addresses WHERE customerID = (%s)) ''')

            cur.execute(sql, customer_id)

            result = cur.fetchall()
            print("address id is", result)
            address_id = result[0]["addressID"]

            sql = (''' UPDATE Customers SET currentAddress = (%s) WHERE customerID = (%s) ''')
            values = (address_id, customer_id)
            cur.execute(sql, values)

            mysql.connection.commit()
            # link = "/pages/addresses.html"

    # establish a mysql connection to retrieve data from DB
    cur = mysql.connection.cursor()

    # retrieve all data from the Foods table to be shown on webpage
    cur.execute('''SELECT * from Foods''')
    foods = cur.fetchall()

    # retrieve all data from the Foods table to be shown on webpage
    cur.execute('''SELECT * from Orders''')
    orders = cur.fetchall()

    # retrieve all data from the Foods table to be shown on webpage
    cur.execute(''' SELECT * FROM OrderItems
                    INNER JOIN Foods
                    ON OrderItems.FoodID = Foods.FoodID''')
    order_items = cur.fetchall()

    # retrieve all data from the Foods table to be shown on webpage
    cur.execute('''SELECT * from Customers''')
    customers = cur.fetchall()

    # retrieve all data from the Foods table to be shown on webpage
    cur.execute('''SELECT * from Addresses''')
    addresses = cur.fetchall()

    # retrieve all data from the Foods table to be shown on webpage
    cur.execute('''SELECT * from Payments''')
    payments = cur.fetchall()
        
    # retrieve address information for each order

    # create an empty list to store address information for each order
    order_addr_info = []

    # iterate througth current orders
    for order in orders:

        # get the customer ID for each order
        print("order is", order)
        customer_id = order["customerID"]

        # fetch the current address for each customer
        cur.execute(''' SELECT currentAddress FROM Customers WHERE customerID = (%s) ''', (customer_id,))

        # obtain the query result
        result = cur.fetchall()

        # get the address ID from the query
        address_id = result[0]["currentAddress"]

        # fetch the DB for the address information for the address ID obtained above
        cur.execute(''' SELECT city, streetName, streetNumber FROM Addresses WHERE addressID = (%s) ''', (address_id, ))

        # get the query result
        result = cur.fetchall()

        address_info = []

        if result:
            # store the address info in a list
            address_info = [result[0]["streetNumber"], result[0]["streetName"], result[0]["city"]]
            
        # append the address info list to the list of addresses for each order
        order_addr_info.append(address_info)

    # render the HTML webpage and attch all data retrieved above to be used by the HTML
    return render_template(link, foods=foods, orders=orders, 
                            order_items=order_items, customers=customers, 
                            addresses=addresses, payments=payments, 
                            food_search=food_search, order_addr_info = order_addr_info)


@app.route("/edit-food", methods=['POST'])
def edit_food():
    # start a mysql connection
        cur = mysql.connection.cursor()

        # obtain the form data received from the request
        data = request.form

        food_id = data["foodID"]
        food_name = data["foodName"]
        food_description = data["foodDescription"]
        food_category = data["foodCategory"]
        cuisine = data["cuisine"]
        calories = data["calories"]
        price = data["price"]

        sql = (''' UPDATE Foods SET foodName = (%s), foodDescription = (%s), 
                    foodCategory = (%s), calories = (%s), cuisine = (%s), 
                    price = (%s) WHERE foodID = (%s) ''')

        values = (food_name, food_description, food_category, calories, cuisine, price, food_id)
        cur.execute(sql, values)
        mysql.connection.commit()
        
        return redirect(url_for(('restaurant_database')))

@app.route("/edit-order", methods=['POST'])
def edit_order():
    # start a mysql connection
        cur = mysql.connection.cursor()

        # obtain the form data received from the request
        data = request.form

        order_id = data["orderID"]
        order_progress = data["orderProgress"]
        order_date = data["orderDate"]

        sql = (''' UPDATE Orders SET orderProgress = (%s), orderDate = (%s) WHERE orderID = (%s) ''')

        values = (order_progress, order_date, order_id)
        cur.execute(sql, values)
        mysql.connection.commit()
        
        return redirect(url_for(('restaurant_database')))

@app.route("/edit-item", methods=['POST'])
def edit_item():
    # start a mysql connection
        cur = mysql.connection.cursor()

        # obtain the form data received from the request
        data = request.form

        order_id = data["orderID"]
        quantity = data["quantity"]
        food_id = data["foodID"]
        item_price = data["totalPrice"]
        # get new total price for order item

        sql = ('''SELECT price FROM Foods WHERE foodID = (%s)''')

        cur.execute(sql, (food_id, ))

        result = cur.fetchall()

        food_price = result[0]["price"]

        total_price = float(food_price) * float(quantity)

        # update order item information

        sql = (''' UPDATE OrderItems SET quantity = (%s), totalPrice = (%s) WHERE orderID = (%s) AND foodID = (%s)''')

        values = (quantity, total_price, order_id, food_id)
        cur.execute(sql, values)

        price_diff = total_price - float(item_price)

        cur.execute(''' SELECT totalPrice FROM Orders WHERE orderID = (%s) ''', (order_id, ))

        result = cur.fetchall()

        order_price = result[0]["totalPrice"]

        updated_price = float(order_price) + price_diff

        sql = ('''UPDATE Orders SET totalPrice = (%s) WHERE orderID = (%s)''')

        values = (updated_price, order_id)

        cur.execute(sql, values)

        mysql.connection.commit()
        
        return redirect(url_for(('restaurant_database')))
        

@app.route("/edit-customer", methods=['POST'])
def edit_customer():
    # start a mysql connection
        cur = mysql.connection.cursor()

        # obtain the form data received from the request
        data = request.form

        customer_id = data["customerID"]
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]
        phone_number = data["phoneNumber"]
        current_address = data["currentAddress"]

        sql = (''' UPDATE Customers SET firstName = (%s), lastName = (%s), email = (%s), phoneNumber = (%s), currentAddress = (%s) WHERE customerID = (%s)''')

        values = (first_name, last_name, email, phone_number, current_address, customer_id)
        cur.execute(sql, values)
        mysql.connection.commit()
        
        return redirect(url_for(('restaurant_database')))


@app.route("/edit-address", methods=['POST'])
def edit_address():
    # start a mysql connection
        cur = mysql.connection.cursor()

        # obtain the form data received from the request
        data = request.form

        address_id = data["addressID"]
        city = data["city"]
        street_name = data["streetName"]
        street_number = data["streetNumber"]

        sql = (''' UPDATE Addresses SET city = (%s), streetName = (%s), streetNumber = (%s) WHERE addressID = (%s)''')

        values = (city, street_name, street_number, address_id)
        cur.execute(sql, values)
        mysql.connection.commit()
        
        return redirect(url_for(('restaurant_database')))



if __name__ == "__main__":

    # starting flask listening socket
    app.run(host='0.0.0.0', debug=True, port=5000)
