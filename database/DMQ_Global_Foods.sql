
-- Customers
-- create 
INSERT INTO `Customers` VALUES (:ID, :web_supplied_AddrID, :web_supplied_fname, :web_supplied_lname, :web_supplied_email, :web_supplied_phone);

-- delete
DELETE FROM Customers WHERE id = :web_supplied_CustomerID OR fname = :web_supplied_fname;

-- update
UPDATE Customers SET fname = :fnameInput, lname= :lnameInput WHERE id= :web_supplied_CustomerId;

-- search
SELECT * from Customers WHERE fname = :web_supplied_fname;
SELECT * from Customers WHERE lname = :web_supplied_lname;

-- ===========================
-- Orders
-- create
INSERT INTO `Orders` VALUES    (;ID, :web_supplied_customerID, ;web_supplied_progress , :web_supplied_price, :web_supplied_date);

-- delete
DELETE FROM Orders WHERE id = :web_supplied_OrderID;

-- update
UPDATE Orders SET fname = :fnameInput, lname= :lnameInput WHERE id= :web_supplied_CustomerId;

-- search
SELECT * from Orders WHERE orderID = :web_supplied_OrderID;
SELECT * from Orders WHERE customerID = :web_supplied_customerID;

-- ===========================
-- OrderItems
-- create
INSERT INTO `OrderItems` VALUES    (:web_supplied_OrderID, :web_supplied_foodID, :web_supplied_quantity, :web_supplied_totalPrice);

-- delete
DELETE FROM OrderItems WHERE id = :web_supplied_OrderItemID;

-- update
UPDATE OrderItems SET quantity = :web_supplied_qunatity WHERE OrderItemId= :web_supplied_OrderItemId;

-- search
SELECT * FROM OrderItems WHERE orderID = :web_supplied_orderID;

-- ===========================
-- Foods
-- create
INSERT INTO `Foods` VALUES     (, :web_supplied_foodName, :web_supplied_foodDesc, :web_supplied_foodCategory, :web_supplied_foodCalory, :web_supplied_cuisine, :web_supplied_price);

-- delete
DELETE FROM Foods WHERE id = :web_supplied_foodID;

-- update
UPDATE Foods SET foodName = :web_supplied_foodName WHERE foodName= :web_supplied_foodName;

-- search
SELECT * FROM Foods WHERE foodName = :web_supplied_foodName;
-- ===========================
-- Payments
-- create
INSERT INTO `Payments` (`paymentID`, `customerID`, `orderID`, `paymentDate`, `paymentAmount`, `paymentMethod`)
VALUES  (:web_supplied_paymentID, :web_supplied_customerID, :web_supplied_orderID, :web_supplied_date, :web_supplied_amount, :web_supplied_payment);

-- delete
DELETE FROM Payments WHERE paymentID = :web_supplied_paymentID;

-- update
UPDATE Payments SET paymentAmount = :web_supplied_amount WHERE paymentId= :web_supplied_paymentId;

-- search
SELECT * FROM Payments WHERE paymentId= :web_supplied_paymentId;

-- ===========================
-- Addresses
-- create
INSERT INTO `Addresses` VALUES (:web_supplied_addressId, :web_supplied_city, :web_supplied_streetName, :web_supplied_streetNumber);

-- delete
DELETE FROM Addresses WHERE addressId = :web_supplied_ID;

-- update
UPDATE Addresses SET city = :web_supplied_city WHERE addressID= :web_supplied_Id;
UPDATE Addresses SET streetName = :web_supplied_street WHERE addressID= :web_supplied_Id;
UPDATE Addresses SET streetNumber = :web_supplied_streetNumber WHERE addressID= :web_supplied_Id;

-- search
SELECT * FROM Addresses WHERE addressID = :web_supplied_ID;
