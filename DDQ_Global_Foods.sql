

--
-- Table structure for table `Foods`
--

DROP TABLE IF EXISTS `payments`;
DROP TABLE IF EXISTS `orderItems`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `customers`;
DROP TABLE IF EXISTS `addresses`;
DROP TABLE IF EXISTS `foods`;

CREATE TABLE `foods` (
  `foodID`          int NOT NULL AUTO_INCREMENT,
  `foodName`        varchar(50) NOT NULL,
  `foodDescription` varchar(255) NOT NULL,
  `foodCategory`    varchar(50) NOT NULL,
  `calories`        int(10) NOT NULL,
  `cuisine`         varchar(50) NOT NULL,
  `price`           float NOT NULL,
  PRIMARY KEY (`foodID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Foods`
--

INSERT INTO `foods` VALUES     (1, 'Mangolian Beef', 'Stir fryed sliced flank steak with soy sauce and green onions', 'Main Dishes', 800, 'Chinese', 20.50),
                               (2, 'Sugarcane Juice', 'Delicious juice made from sugarcanes imported from Thaliand', 'Drinks', 150, 'Thai', 4.50),
                               (3, 'Zurek', 'Fermented soup made with sour rye flour', 'Appetizers', 120, 'Polish', 8.50);


--
-- Table structure for table `Addresses`
--

DROP TABLE IF EXISTS `addresses`;

CREATE TABLE `addresses` (
  `addressID`       int NOT NULL AUTO_INCREMENT,
  `city`            varchar(50) NOT NULL,
  `streetName`      varchar(50) NOT NULL,
  `streetNumber`    int NOT NULL,
  PRIMARY KEY (`addressID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Addresses`
--

INSERT INTO `addresses` VALUES (1, 'Boston', 'Raven Street', 25345),
                               (2, 'Dallas', '6th Avenue', 235523),
                               (3, 'Sao Paolo', 'Church Road', 55643);


--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `customerID`      int NOT NULL AUTO_INCREMENT,
  `currentAddress`  int DEFAULT NULL,
  `firstName`       varchar(50) NOT NULL,
  `lastName`        varchar(50) NOT NULL,
  `email`           varchar(70) NOT NULL,
  `phoneNumber`     int NOT NULL,
  PRIMARY KEY (`customerID`),
  KEY `currentAddress` (`currentAddress`),
  FOREIGN KEY (`currentAddress`) REFERENCES `addresses` (`addressID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Customers`
--

INSERT INTO `customers` VALUES (1, 1, 'Alfred', 'Clark', 'alf.clark@hotmail.com', 021244812),
                               (2, 2, 'Lisa', 'Young', 'lisa-1992k@gmail.com', 021349553),
                               (3, 3, 'Ali', 'Omer', 'ali-omer@yahoo.com', 021140012);



--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `orderID`         int NOT NULL AUTO_INCREMENT,
  `customerID`      int NOT NULL,
  `orderProgress`   varchar(50) NOT NULL,
  `totalPrice`      float NOT NULL,
  `orderDate`       date NOT NULL,
  PRIMARY KEY (`orderID`),
  KEY `customerID` (`customerID`),
  FOREIGN KEY (`customerID`) REFERENCES `customers` (`customerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Orders`
--

INSERT INTO `orders` VALUES    (1, 1, 'New', 41.00, STR_TO_DATE('02/12/2021', '%m/%d/%Y')),
                               (2, 2, 'Preparing', 13.50, STR_TO_DATE('02/09/2021', '%m/%d/%Y')),
                               (3, 3, 'Delivered', 25.50, STR_TO_DATE('01/23/2021', '%m/%d/%Y'));


--
-- Table structure for table `OrderItems`
--

DROP TABLE IF EXISTS `orderItems`;

CREATE TABLE `orderItems` (
  `orderID`         int NOT NULL,
  `foodID`          int NOT NULL,
  `quantity`        int NOT NULL,
  `totalPrice`      float NOT NULL,
  KEY `orderID` (`orderID`),
  KEY `foodID` (`foodID`),
  FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderID`),
  FOREIGN KEY (`foodID`) REFERENCES `foods` (`foodID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `OrderItems`
--

INSERT INTO `orderItems` VALUES    (1, 1, 2, 41.00),
                               (2, 2, 3, 13.50),
                               (3, 3, 3, 25.50);


--
-- Table structure for table `Payments`
--

DROP TABLE IF EXISTS `payments`;

CREATE TABLE `payments` (
  `paymentID`      int NOT NULL AUTO_INCREMENT,
  `customerID`     int NOT NULL,
  `orderID`        int NOT NULL,
  `paymentDate`    date NOT NULL,
  `paymentAmount`  float NOT NULL,
  `paymentMethod`  varchar(50) NOT NULL,
  PRIMARY KEY (`paymentID`),
  KEY `customerID` (`customerID`),
  KEY `orderID` (`orderID`),
  FOREIGN KEY (`customerID`) REFERENCES `customers` (`customerID`),
  FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Payments`
--

INSERT INTO `payments` (`paymentID`, `customerID`, `orderID`, `paymentDate`, `paymentAmount`, `paymentMethod`)
VALUES  (1, 1, 1, STR_TO_DATE('02/12/2021', '%m/%d/%Y'), 41.00, 'Credit Card'),
        (2, 2, 2, STR_TO_DATE('02/09/2021', '%m/%d/%Y'), 13.50, 'Credit Card'),
        (3, 3, 3, STR_TO_DATE('01/23/2021', '%m/%d/%Y'), 25.50, 'Cash');
