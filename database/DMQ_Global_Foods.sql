

-- Foods
-- create
INSERT INTO Foods (foodName, foodDescription, foodCategory, calories, cuisine, price)
VALUES (web_supplied_foodName, :web_supplied_foodDesc, :web_supplied_foodCategory, :web_supplied_foodCalories, :web_supplied_cuisine, :web_supplied_price);

-- delete
DELETE FROM Foods WHERE foodID = :web_supplied_foodID;

-- update
UPDATE Foods SET foodName = :web_supplied_foodName, foodDescription= :web_supplied_foodDesc, foodCategory, calories = :web_supplied_foodCalories, cuisine = :web_supplied_cuisine WHERE foodID= :web_supplied_foodID;

-- search
SELECT * FROM Foods WHERE foodName LIKE :web_supplied_foodName;

-- ===========================

-- Customers
-- create 
INSERT INTO Customers (firstName, lastName, email, phoneNumber)
VALUES (:web_supplied_fname, :web_supplied_lname, :web_supplied_email, :web_supplied_phone);
-- delete
DELETE FROM Customers WHERE id = :web_supplied_CustomerID;

-- update
UPDATE Customers SET fname = :fnameInput, lname= :lnameInput, email= :emailInput, phoneNumber= :phoneNumberInput WHERE customerID= :web_supplied_CustomerId;


-- ===========================

-- Addresses
-- create
INSERT INTO Addresses (customerID, city, streetName, streetNumber)
VALUES (:web_supplied_customerID, :web_supplied_city, :web_supplied_streetName, :web_supplied_streetNumber);

-- delete
DELETE FROM Addresses WHERE addressId = :web_supplied_ID;

-- update
UPDATE Addresses SET city = :web_supplied_city, streetName = :web_supplied_street, streetNumber = :web_supplied_streetNumber WHERE addressID= :web_supplied_Id;

-- ===========================

-- Orders
-- create
INSERT INTO Orders (customerID, orderProgress, orderDate)
VALUES    (:web_supplied_customerID, ;web_supplied_progress, :web_supplied_date);

-- delete
DELETE FROM Orders WHERE id = :web_supplied_OrderID;

-- update order
UPDATE Orders SET orderProgress = :orderProgressInput, orderDate= :orderDateInput WHERE orderID= :web_supplied_orderID;

-- update order price according to the collective price of order items inside that order
SELECT SUM(totalPrice) as totalPrice FROM OrderItems WHERE orderID = :web_supplied_orderID;
UPDATE Orders SET totalPrice = totalPrice


-- ===========================
-- OrderItems
-- create
INSERT INTO OrderItems (orderID, foodID, quantity)
VALUES    (:web_supplied_OrderID, :web_supplied_foodID, :web_supplied_quantity);

-- delete
DELETE FROM OrderItems WHERE orderID = :web_supplied_orderID AND foodID = :web_supplied_foodID;

-- update order item
UPDATE OrderItems SET quantity = :web_supplied_qunatity WHERE orderID = :web_supplied_orderID AND foodID = :web_supplied_foodID;

-- update order item price according to the quantity of foods inside that item
SELECT price AS food_price FROM Foods WHERE foodID = :web_supplied_foodID;
SELECT quantity AS food_quantity FROM OrderItems WHERE foodID = :web_supplied_foodID;
UPDATE OrderItems SET totalPrice = food_price * food_quantity WHERE foodID = :web_supplied_foodID;


-- ===========================
-- Payments
-- create
INSERT INTO Payments (customerID, orderID, paymentDate, paymentAmount, paymentMethod)
VALUES  (:web_supplied_customerID, :web_supplied_orderID, :web_supplied_date, :web_supplied_amount, :web_supplied_payment);

-- delete
DELETE FROM Payments WHERE paymentID = :web_supplied_paymentID;





