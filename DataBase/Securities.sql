CREATE DATABASE Securities;
USE Securities;

CREATE TABLE Industry (
industryID INT PRIMARY KEY AUTO_INCREMENT,
keyword VARCHAR(255) NOT NULL,
description TEXT(200)
);

CREATE TABLE Company (
companyID INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100) NOT NULL,
createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
totalAssets DECIMAL(15, 2),
revenue DECIMAL(15, 2),
employeeCount INT,
currentScore DECIMAL(5, 2),
foundedYear YEAR,
industryID INT,
FOREIGN KEY (industryID) REFERENCES Industry(industryID)
);

CREATE TABLE CompanyWebsite (
websiteID INT PRIMARY KEY AUTO_INCREMENT,
companyID INT,
url VARCHAR(255) NOT NULL,
FOREIGN KEY (companyID) REFERENCES Company(companyID)
);

CREATE TABLE Article (
articleID INT PRIMARY KEY AUTO_INCREMENT,
updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
link VARCHAR(255),
companyID INT,
FOREIGN KEY (companyID) REFERENCES Company(companyID)
);

CREATE TABLE PriceHistory (
priceID INT PRIMARY KEY AUTO_INCREMENT,
price DECIMAL(15, 2),
updatedAt DATETIME,
companyID INT,
FOREIGN KEY (companyID) REFERENCES Company(companyID)
);

CREATE TABLE ScoreHistory (
scoreID INT PRIMARY KEY AUTO_INCREMENT,
score DECIMAL(5, 2),
updatedAt DATETIME,
companyID INT,
FOREIGN KEY (companyID) REFERENCES Company(companyID),
CONSTRAINT CHK_Score_Range CHECK (score >= 0)
);

INSERT INTO Industry (keyword, description)
VALUES
('Technology', 'Companies involved in technology-related products and services.'),
('Finance', 'Companies involved in financial services and activities.'),
('Healthcare', 'Companies involved in healthcare and medical services.'),
('Manufacturing', 'Companies involved in manufacturing and production processes.');

INSERT INTO Company (name, totalAssets, revenue, employeeCount, currentScore, foundedYear, industryID)
VALUES
('ABC Corp', 1000000.00, 500000.00, 50, 75.50, 2005, 1),
('XYZ Inc', 2000000.00, 800000.00, 100, 85.00, 2010, 2),
('123 Industries', 1500000.00, 600000.00, 75, 70.25, 2008, 3),
('Tech Solutions Ltd', 3000000.00, 1200000.00, 200, 90.75, 2015, 4);

INSERT INTO CompanyWebsite (companyID, url)
VALUES
(1, 'http://www.abccorp.com'),
(2, 'http://www.xyzinc.com'),
(3, 'http://www.123industries.com'),
(4, 'http://www.techsolutionsltd.com');

INSERT INTO Article (link, companyID)
VALUES
('http://www.example.com/article1', 1),
('http://www.example.com/article2', 2),
('http://www.example.com/article3', 3),
('http://www.example.com/article4', 4);

INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(1000.50, '2024-02-15 12:30:00', 1),
(1500.75, '2024-02-15 13:45:00', 2),
(800.25, '2024-02-15 14:20:00', 3),
(2000.00, '2024-02-15 15:10:00', 4);

INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(75.50, '2024-02-15 12:30:00', 1),
(85.00, '2024-02-15 13:45:00', 2),
(70.25, '2024-02-15 14:20:00', 3),
(90.75, '2024-02-15 15:10:00', 4),
(78.00, '2024-02-14 12:30:00', 1),
(83.25, '2024-02-14 13:45:00', 2),
(68.75, '2024-02-14 14:20:00', 3),
(88.00, '2024-02-14 15:10:00', 4),
(75.00, '2024-02-13 12:30:00', 1),
(80.25, '2024-02-13 13:45:00', 2),
(65.50, '2024-02-13 14:20:00', 3),
(85.50, '2024-02-13 15:10:00', 4);

