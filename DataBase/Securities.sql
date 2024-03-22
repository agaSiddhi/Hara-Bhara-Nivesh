CREATE DATABASE Securities;
USE Securities;

CREATE TABLE Industry (
industryID INT PRIMARY KEY AUTO_INCREMENT,
keyword VARCHAR(255) NOT NULL,
description TEXT(200)
);

CREATE TABLE Company (
companyID VARCHAR(50) PRIMARY KEY,
name VARCHAR(100) NOT NULL,
createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
totalAssets DECIMAL(15, 2),
revenue DECIMAL(15, 2),
employeeCount INT,
currentScore DECIMAL(5, 2),
foundedYear YEAR,
industryID INT,
fundCategory VARCHAR(100),
wallet DECIMAL(15, 2),
FOREIGN KEY (industryID) REFERENCES Industry(industryID)
);

CREATE TABLE CompanyWebsite (
websiteID INT PRIMARY KEY AUTO_INCREMENT,
companyID VARCHAR(50),
url VARCHAR(255) NOT NULL,
FOREIGN KEY (companyID) REFERENCES Company(companyID)
);

CREATE TABLE Article (
articleID INT PRIMARY KEY AUTO_INCREMENT,
updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
link VARCHAR(255),
companyID VARCHAR(50),
FOREIGN KEY (companyID) REFERENCES Company(companyID)
);

CREATE TABLE PriceHistory (
priceID INT PRIMARY KEY AUTO_INCREMENT,
price DECIMAL(15, 2),
updatedAt DATETIME,
companyID VARCHAR(50),
FOREIGN KEY (companyID) REFERENCES Company(companyID)
);

CREATE TABLE ScoreHistory (
scoreID INT PRIMARY KEY AUTO_INCREMENT,
score DECIMAL(5, 2),
updatedAt DATETIME,
companyID VARCHAR(50),
FOREIGN KEY (companyID) REFERENCES Company(companyID),
CONSTRAINT CHK_Score_Range CHECK (score >= 0)
);

CREATE TABLE User(
username VARCHAR(255) PRIMARY KEY,
balance DECIMAL(15, 2) NOT NULL,
name VARCHAR(255) NOT NULL,
password VARCHAR(60) NOT NULL,
age ENUM ('<18', '18-29', '30-44','45-60','>60'),
country VARCHAR(50),
gender ENUM ('Female', 'Male', 'Others')
);

CREATE TABLE User_mail(
username VARCHAR(255),
email VARCHAR(255) NOT NULL ,
FOREIGN KEY (username) REFERENCES User(username),
PRIMARY KEY (username,email)
);

CREATE TABLE Transaction_history(
transactionID INT PRIMARY KEY AUTO_INCREMENT,
price_quote DECIMAL(15, 2),
date DATETIME,
order_type ENUM('Buy', 'Sell'),
amount DECIMAL(15, 2),
Ticker VARCHAR(50),
username VARCHAR(255),
FOREIGN KEY (Ticker) REFERENCES Company(companyID),
FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE Portfolio_entry(
portfolioEntryID INT PRIMARY KEY AUTO_INCREMENT,
price_quote DECIMAL(15, 2),
date DATETIME,
order_type ENUM('Buy', 'Sell'),
amount DECIMAL(15, 2),
Ticker VARCHAR(50),
username VARCHAR(255),
FOREIGN KEY (Ticker) REFERENCES Company(companyID),
FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE Bid(
bidID INT PRIMARY KEY AUTO_INCREMENT,
initial_Bid DECIMAL(15, 2),
minimum_Step DECIMAL(5, 2),
credits_Listed INT,
companyID VARCHAR(50),
FOREIGN KEY (CompanyID) REFERENCES CompanySignup(CompanyTicker)
);

CREATE TABLE Bidding(
bidder VARCHAR(50),
bidID INT,
bid DECIMAL(15, 2),
FOREIGN KEY (bidder) REFERENCES CompanySignup(CompanyTicker),
FOREIGN KEY (bidID) REFERENCES Bid(bidID),
PRIMARY KEY(bidder,bidID)
);

CREATE TABLE CompanySignup (
CompanyName VARCHAR(255) NOT NULL,
CompanyTicker VARCHAR(10) PRIMARY KEY,
Password VARCHAR(255) NOT NULL,
InitialMoneyWalletBalance DECIMAL(18, 2) DEFAULT 0,
InitialCreditsWalletBalance DECIMAL(18, 2) DEFAULT 0,
fundCategory VARCHAR(100),
industryID INT,
FOREIGN KEY (industryID) REFERENCES Industry(industryID)
);

CREATE TABLE ESG (
ID INT AUTO_INCREMENT PRIMARY KEY,
Environmental DECIMAL(5, 2),
Social DECIMAL(5, 2),
Governance DECIMAL(5, 2),
companyID VARCHAR(50),
FOREIGN KEY (companyID) REFERENCES Company(companyID)
);

CREATE TABLE Article_data (
ID INT AUTO_INCREMENT PRIMARY KEY,
Heading VARCHAR(255),
Text TEXT,
Datetime DATETIME,
Company VARCHAR(255),
Category VARCHAR(50),
Score FLOAT,
Score_blob FLOAT
);

CREATE TABLE esg_ratings (
ID INT AUTO_INCREMENT PRIMARY KEY,
Company VARCHAR(255),
ESG_Risk_Rating VARCHAR(255),
Score FLOAT
);

CREATE TABLE esg_data (
id INT AUTO_INCREMENT PRIMARY KEY,
company_name VARCHAR(255),
date DATE,
environment FLOAT,
social FLOAT,
governance FLOAT,
esg_ratings VARCHAR(255),
final_esg_score FLOAT,
historical_esg_score FLOAT
);

INSERT INTO Industry (keyword, description) VALUES
('Capital Goods', 'Companies involved in manufacturing and distribution of industrial equipment and machinery.'),
('Financial', 'Financial institutions including banks, investment firms, and insurance companies.'),
('Services', 'Companies providing various types of services such as consulting, IT services, and hospitality.'),
('HealthCare', 'Companies involved in healthcare services, pharmaceuticals, and medical equipment manufacturing.'),
('Consumer Staples', 'Manufacturers and distributors of essential consumer goods like food, beverages, and household products.'),
('Other', 'Industries that do not fit into the defined categories or are niche markets.');

INSERT INTO Company (companyID, name, industryID, totalAssets, revenue, employeeCount, currentScore, foundedYear, fundCategory,wallet) VALUES
('CAAMX.SA', 'China Asset Management Co.', 2, 206574520000, 7802380000, 13947, 60.504, 1998, 'Equity', 300),
('CSMF.PA', 'AXA S.A.', 2, 734040000000, 107831000000, 149000, 74.77, 1946, 'Equity', 300),
('UBSG.SW', 'UBS Group AG', 2, 1104364000000, 97975000000, 83560, 71.24, 1998, 'Hybrid', 300),
('JEF', 'Jefferies Financial Group Inc.', 1, 440000000000, 8200000000, 5381, 67.75, 1962, 'Hybrid', 300),
('HNNMY', 'H&M Hennes & Mauritz AB', 5, 21710000000, 24800000000, 107375, 38.87, 1947, 'Debt', 300),
('MSCI', 'MSCI Inc.', 3, 5518000000, 530000000, 5794, 64.66, 1969, 'Debt', 300),
('KPMGY', 'KPMG', 3, 35000000000, 36400000000, 273424, 64.64, 1987, 'Others', 300),
('EXK', 'Endeavour Silver Corp.', 5, 12000000000, 300000000, 73424, 50.4, 1981, 'Others', 300),
('PM', 'Philip Morris International Inc.', 4, 21200000000, 3176200000, 123432, 44.74, 1947, 'Equity', 300), 
('UBP', 'Union Bancaire Privée UBP SA', 2, 140400000000, 145300000, 1960, 61.77, 1969, 'Others', 300),
('MET', 'MetLife Inc.', 4, 19800000000, 1700000, 430000, 58.16, 1968, 'Debt', 300),
('BCS', 'Barclays PLC', 3, 188000000000, 32120000000, 81000, 47.76, 1990, 'Hybrid', 300),
('AMZN', 'Amazon.com Inc.', 6, 527900000000, 30430000000, 1525000, 51.33, 1994, 'Equity', 300),
('IMPACT.CO', 'Impact Coatings AB', 6, 52000000, 300000, 25000, 50.9, 1997, 'Equity', 300),
('BLK', 'BlackRock  Inc.', 2, 1000000000000, 17850000000, 19000, 24.62, 1988, 'Debt', 300),
('XOM', 'Exxon Mobil Corporation', 6, 376300000000, 344600000000, 61500, 62.13, 1999, 'Others', 300),
('NOVN.SW', 'Novartis International AG', 5, 52000000, 450000, 5000, 59.39, 1996, 'Hybrid', 300);

INSERT INTO CompanyWebsite (companyID, url) VALUES
('CAAMX.SA', 'https://en.chinaamc.com'),
('CSMF.PA', 'https://www.axa.com'),
('UBSG.SW', 'https://www.ubs.com/global/en/our-firm/governance/ubs-group-ag.html'),
('JEF', 'https://www.jefferies.com'),
('HNNMY', 'https://www2.hm.com/en_in/index.html'),
('MSCI', 'https://www.msci.com'),
('KPMGY', 'https://kpmg.com/xx/en/home.html'),
('EXK', 'https://edrsilver.com'),
('PM', 'https://www.pmi.com'),
('UBP', 'https://www.ubp.com/en'),
('MET', 'https://www.metlife.com'),
('BCS', 'https://home.barclays'),
('AMZN', 'https://ir.aboutamazon.com/overview/default.aspx'),
('IMPACT.CO', 'https://impactcoatings.com'),
('BLK', 'https://www.blackrock.com/corporate/global-directory'),
('XOM', 'https://corporate.exxonmobil.com'),
('NOVN.SW', 'https://www.novartis.com');

-- Data for ScoreHistory table for China Asset Management Co.
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(56.78, '2023-01-26', 'CAAMX.SA'),
(59.55, '2024-01-01', 'CAAMX.SA'),
(60, '2024-02-15', 'CAAMX.SA'),
(59.54, '2024-03-04', 'CAAMX.SA'),
(60.5, '2024-03-18', 'CAAMX.SA');

-- Data for ScoreHistory table for AXA S.A. 
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(62.72, '2023-02-26', 'CSMF.PA'),
(76.23, '2024-01-01', 'CSMF.PA'),
(72.4, '2024-02-15', 'CSMF.PA'),
(74.55, '2024-03-04', 'CSMF.PA'),
(74.76, '2024-03-18', 'CSMF.PA');

-- Data for ScoreHistory table for UBS Group AG
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(62.05, '2023-03-06', 'UBSG.SW'),
(72.28, '2024-01-01', 'UBSG.SW'),
(69.53, '2024-02-15', 'UBSG.SW'),
(72.28, '2024-03-04', 'UBSG.SW'),
(71.24, '2024-03-18', 'UBSG.SW');

-- Data for ScoreHistory table for Jefferies Financial Group Inc. 
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(60.80, '2023-03-24', 'JEF'),
(67.98, '2024-01-01', 'JEF'),
(67.66, '2024-02-15', 'JEF'),
(68.6, '2024-03-04', 'JEF'),
(67.76, '2024-03-18', 'JEF');

-- Data for ScoreHistory table for H&M Hennes & Mauritz AB 
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(37.97, '2023-04-03', 'HNNMY'),
(37.13, '2024-01-01', 'HNNMY'),
(38.09, '2024-02-15', 'HNNMY'),
(38.94, '2024-03-04', 'HNNMY'),
(38.84, '2024-03-18', 'HNNMY');

-- Data for ScoreHistory table for MSCI Inc. 
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(64.45, '2023-04-03', 'MSCI'),
(64.38, '2024-01-01', 'MSCI'),
(64.63, '2024-02-15', 'MSCI'),
(64.68, '2024-03-04', 'MSCI'),
(64.66, '2024-03-18', 'MSCI');

-- Data for ScoreHistory table for KPMG
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(64.07, '2023-04-23', 'KPMGY'),
(64.71, '2024-01-01', 'KPMGY'),
(64.77, '2024-02-15', 'KPMGY'),
(64.73, '2024-03-04', 'KPMGY'),
(64.64, '2024-03-18', 'KPMGY');

-- Data for ScoreHistory table for Endeavour Silver Corp.
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(49.34, '2023-05-16', 'EXK'),
(50.13, '2024-01-01', 'EXK'),
(50.14, '2024-02-15', 'EXK'),
(50.66, '2024-03-04', 'EXK'),
(50.41, '2024-03-18', 'EXK');

-- Data for ScoreHistory table for Philip Morris International Inc.
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(44.23, '2023-06-21', 'PM'),
(44.87, '2024-01-01', 'PM'),
(44.90, '2024-02-15', 'PM'),
(44.84, '2024-03-04', 'PM'),
(44.74, '2024-03-18', 'PM');

-- Data for ScoreHistory table for Union Bancaire Privée UBP SA
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(61.28, '2023-07-11', 'UBP'),
(61.85, '2024-01-01', 'UBP'),
(61.91, '2024-02-15', 'UBP'),
(61.86, '2024-03-04', 'UBP'),
(61.78, '2024-03-18', 'UBP');

-- Data for ScoreHistory table for MetLife Inc.
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(57.11, '2023-07-13', 'MET'),
(59.98, '2024-01-01', 'MET'),
(58.90, '2024-02-15', 'MET'),
(58.45, '2024-03-04', 'MET'),
(58.16, '2024-03-18', 'MET');

-- Data for ScoreHistory table for Barclays PLC
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(46.96, '2023-07-18', 'BCS'),
(48.57, '2024-01-01', 'BCS'),
(48.22, '2024-02-15', 'BCS'),
(47.96, '2024-03-04', 'BCS'),
(47.76, '2024-03-18', 'BCS');

-- Data for ScoreHistory table for Amazon.com Inc.
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(51.02, '2023-07-29', 'AMZN'),
(51.19, '2024-01-01', 'AMZN'),
(51.36, '2024-02-15', 'AMZN'),
(51.37, '2024-03-04', 'AMZN'),
(51.34, '2024-03-18', 'AMZN');

-- Data for ScoreHistory table for Impact Coatings AB
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(50.45, '2023-11-29', 'IMPACT.CO'),
(50.65, '2024-01-01', 'IMPACT.CO'),
(51.02, '2024-02-15', 'IMPACT.CO'),
(50.93, '2024-03-04', 'IMPACT.CO'),
(50.90, '2024-03-18', 'IMPACT.CO');

-- Data for ScoreHistory table for BlackRock Inc.
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(23.38, '2023-12-19', 'BLK'),
(24.75, '2024-01-01', 'BLK'),
(24.49, '2024-02-15', 'BLK'),
(24.92, '2024-03-04', 'BLK'),
(24.62, '2024-03-18', 'BLK');

-- Data for ScoreHistory table for Exxon Mobil Corporation
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(61.66, '2024-01-01', 'XOM'),
(61.88, '2024-02-15', 'XOM'),
(62.12, '2024-03-04', 'XOM'),
(62.16, '2024-03-18', 'XOM');

-- Data for ScoreHistory table for Novartis International AG
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(59.10, '2024-02-08', 'NOVN.SW'),
(59.24, '2024-01-01', 'NOVN.SW'),
(59.42, '2024-02-15', 'NOVN.SW'),
(59.44, '2024-03-04', 'NOVN.SW'),
(59.39, '2024-03-18', 'NOVN.SW');

INSERT INTO ESG (Environmental, Social, Governance, companyID) 
VALUES 
(95.56, 60.90, 80.78, 'CAAMX.SA'),
(55.23, 75.57, 70.90, 'CSMF.PA'),
(70.57, 80.23, 90.68, 'UBSG.SW'),
(3.68, 65.23, 93.68, 'JEF'),
(18.57, 61.23, 55.46, 'HNNMY'),
(87.68, 41.90, 42.46, 'MSCI'),
(95.90, 80.90, 50.46, 'KPMGY'),
(49.90, 66.23, 45.46, 'EXK'),
(65.90, 71.90, 17.68, 'PM'),
(97.68, 50.23, 30.90, 'UBP'),
(62.68, 91.90, 57.68, 'MET'),
(53.23, 93.90, 16.79, 'BCS'),
(58.68, 31.57, 84.01, 'AMZN'),
(67.46, 22.46, 53.79, 'IMPACT.CO'),
(36.90, 6.01, 31.23, 'BLK'),
(84.90, 44.79, 35.46, 'XOM'),
(87.90, 50.01, 32.23, 'NOVN.SW');

SELECT name,currentScore, (SELECT description FROM Industry WHERE Company.industryID = Industry.industryID)  FROM Company ORDER BY currentScore DESC;

-- DELIMITER $$
-- CREATE TRIGGER validate_email
-- BEFORE INSERT ON Users
-- FOR EACH ROW
-- BEGIN
--     IF NEW.Email NOT REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Invalid email address';
--     END IF;
-- END$$
-- DELIMITER ;

SELECT * FROM Transaction_history;
SELECT * FROM PriceHistory WHERE updatedAt='2024-02-29' and companyID='XOM';

-- Inserting 20 mock entries into User table
INSERT INTO User (username, balance, name, password, age, country, gender)
VALUES 
    ('user1', 1000.00, 'John Doe', 'password1', '30-44', 'United States', 'Male'),
    ('user2', 500.50, 'Jane Smith', 'password2', '<18', 'Canada', 'Female'),
    ('user3', 750.25, 'Michael Johnson', 'password3', '18-29', 'Australia', 'Male'),
    ('user4', 1500.75, 'Emma Brown', 'password4', '>60', 'United Kingdom', 'Female'),
    ('user5', 200.00, 'Alex Lee', 'password5', '45-60', 'Germany', 'Others'),
    ('user6', 1200.00, 'Emily White', 'password6', '30-44', 'France', 'Female'),
    ('user7', 700.50, 'David Lee', 'password7', '18-29', 'Japan', 'Male'),
    ('user8', 850.25, 'Sophia Miller', 'password8', '<18', 'Brazil', 'Female'),
    ('user9', 1300.75, 'William Taylor', 'password9', '>60', 'Italy', 'Male'),
    ('user10', 150.00, 'Olivia Brown', 'password10', '45-60', 'Spain', 'Female'),
    ('user11', 1800.00, 'Daniel Wilson', 'password11', '30-44', 'Mexico', 'Male'),
    ('user12', 950.50, 'Mia Garcia', 'password12', '<18', 'Argentina', 'Female'),
    ('user13', 550.25, 'James Martinez', 'password13', '18-29', 'South Africa', 'Male'),
    ('user14', 1400.75, 'Ava Rodriguez', 'password14', '>60', 'India', 'Female'),
    ('user15', 300.00, 'Logan Hernandez', 'password15', '45-60', 'China', 'Male'),
    ('user16', 1600.00, 'Ella Gonzalez', 'password16', '30-44', 'Russia', 'Female'),
    ('user17', 1050.50, 'Noah Lopez', 'password17', '<18', 'Nigeria', 'Male'),
    ('user18', 650.25, 'Charlotte Perez', 'password18', '18-29', 'Egypt', 'Female'),
    ('user19', 1700.75, 'Liam Sanchez', 'password19', '>60', 'Germany', 'Male'),
    ('user20', 400.00, 'Harper Ramirez', 'password20', '45-60', 'Canada', 'Female');

-- Inserting 20 mock entries into User_mail table
INSERT INTO User_mail (username, email)
VALUES
    ('user1', 'user1@example.com'),
    ('user2', 'user2@example.com'),
    ('user3', 'user3@example.com'),
    ('user4', 'user4@example.com'),
    ('user5', 'user5@example.com'),
    ('user6', 'user6@example.com'),
    ('user7', 'user7@example.com'),
    ('user8', 'user8@example.com'),
    ('user9', 'user9@example.com'),
    ('user10', 'user10@example.com'),
    ('user11', 'user11@example.com'),
    ('user12', 'user12@example.com'),
    ('user13', 'user13@example.com'),
    ('user14', 'user14@example.com'),
    ('user15', 'user15@example.com'),
    ('user16', 'user16@example.com'),
    ('user17', 'user17@example.com'),
    ('user18', 'user18@example.com'),
    ('user19', 'user19@example.com'),
    ('user20', 'user20@example.com');
    
    
-- Inserting transaction history for user1
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (100.00, '2024-03-21 10:00:00', 'Buy', 10, 'CAAMX.SA', 'user1'),
    (110.00, '2024-03-21 11:30:00', 'Sell', 5, 'CSMF.PA', 'user1'),
    (90.00, '2024-03-21 13:45:00', 'Buy', 8, 'UBSG.SW', 'user1');
    
-- Inserting portfolio entry for user1
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (100.00, '2024-03-21 10:00:00', 'Buy', 10, 'CAAMX.SA', 'user1'),
    (110.00, '2024-03-21 11:30:00', 'Sell', 5, 'CSMF.PA', 'user1'),
    (90.00, '2024-03-21 13:45:00', 'Buy', 8, 'UBSG.SW', 'user1');

-- Inserting transaction history for user2
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (50.00, '2024-03-21 09:30:00', 'Buy', 5, 'JEF', 'user2'),
    (55.00, '2024-03-21 14:00:00', 'Sell', 3, 'HNNMY', 'user2');
    
-- Inserting portfolio entry for user2
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (50.00, '2024-03-21 09:30:00', 'Buy', 5, 'JEF', 'user2'),
    (55.00, '2024-03-21 14:00:00', 'Sell', 3, 'HNNMY', 'user2');

-- Inserting transaction history for user3
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 10:45:00', 'Buy', 12, 'MSCI', 'user3'),
    (130.00, '2024-03-21 12:15:00', 'Sell', 7, 'KPMGY', 'user3'),
    (115.00, '2024-03-21 14:30:00', 'Buy', 10, 'EXK', 'user3');
    
-- Inserting portfolio entry for user3
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 10:45:00', 'Buy', 12, 'MSCI', 'user3'),
    (130.00, '2024-03-21 12:15:00', 'Sell', 7, 'KPMGY', 'user3'),
    (115.00, '2024-03-21 14:30:00', 'Buy', 10, 'EXK', 'user3');

-- Inserting transaction history for user4
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (75.00, '2024-03-21 11:00:00', 'Buy', 8, 'PM', 'user4');
    
-- Inserting portfolio entry for user4
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (75.00, '2024-03-21 11:00:00', 'Buy', 8, 'PM', 'user4');

-- Inserting transaction history for user5
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (200.00, '2024-03-21 10:30:00', 'Buy', 2, 'UBP', 'user5'),
    (190.00, '2024-03-21 12:00:00', 'Sell', 1, 'MET', 'user5');
    
-- Inserting portfolio entry for user5
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (200.00, '2024-03-21 10:30:00', 'Buy', 2, 'UBP', 'user5'),
    (190.00, '2024-03-21 12:00:00', 'Sell', 1, 'MET', 'user5');

-- Inserting transaction history for user6
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (80.00, '2024-03-21 09:00:00', 'Buy', 7, 'BCS', 'user6'),
    (85.00, '2024-03-21 11:30:00', 'Sell', 4, 'AMZN', 'user6'),
    (75.00, '2024-03-21 13:45:00', 'Buy', 5, 'IMPACT.CO', 'user6');
    
-- Inserting portfolio entry for user6
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (80.00, '2024-03-21 09:00:00', 'Buy', 7, 'BCS', 'user6'),
    (85.00, '2024-03-21 11:30:00', 'Sell', 4, 'AMZN', 'user6'),
    (75.00, '2024-03-21 13:45:00', 'Buy', 5, 'IMPACT.CO', 'user6');

-- Inserting transaction history for user7
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 09:30:00', 'Buy', 12, 'BLK', 'user7'),
    (125.00, '2024-03-21 12:00:00', 'Sell', 6, 'XOM', 'user7');
    
-- Inserting portfolio entry for user7
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 09:30:00', 'Buy', 12, 'BLK', 'user7'),
    (125.00, '2024-03-21 12:00:00', 'Sell', 6, 'XOM', 'user7');

-- Inserting transaction history for user8
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (95.00, '2024-03-21 10:45:00', 'Buy', 8, 'NOVN.SW', 'user8'),
    (100.00, '2024-03-21 13:15:00', 'Sell', 4, 'MSCI', 'user8'),
    (90.00, '2024-03-21 14:30:00', 'Buy', 6, 'KPMGY', 'user8');
    
-- Inserting portfolio entry for user8
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (95.00, '2024-03-21 10:45:00', 'Buy', 8, 'NOVN.SW', 'user8'),
    (100.00, '2024-03-21 13:15:00', 'Sell', 4, 'MSCI', 'user8'),
    (90.00, '2024-03-21 14:30:00', 'Buy', 6, 'KPMGY', 'user8');

-- Inserting transaction history for user9
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (150.00, '2024-03-21 11:00:00', 'Buy', 10, 'EXK', 'user9'),
    (155.00, '2024-03-21 13:30:00', 'Sell', 5, 'PM', 'user9'),
    (145.00, '2024-03-21 14:45:00', 'Buy', 8, 'UBP', 'user9');
    
-- Inserting portfolio entry for user9
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (150.00, '2024-03-21 11:00:00', 'Buy', 10, 'EXK', 'user9'),
    (155.00, '2024-03-21 13:30:00', 'Sell', 5, 'PM', 'user9'),
    (145.00, '2024-03-21 14:45:00', 'Buy', 8, 'UBP', 'user9');

-- Inserting transaction history for user10
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (70.00, '2024-03-21 10:00:00', 'Buy', 6, 'MET', 'user10'),
    (75.00, '2024-03-21 12:30:00', 'Sell', 3, 'BCS', 'user10'),
    (65.00, '2024-03-21 14:15:00', 'Buy', 5, 'AMZN', 'user10');
    
-- Inserting portfolio entry for user10
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (70.00, '2024-03-21 10:00:00', 'Buy', 6, 'MET', 'user10'),
    (75.00, '2024-03-21 12:30:00', 'Sell', 3, 'BCS', 'user10'),
    (65.00, '2024-03-21 14:15:00', 'Buy', 5, 'AMZN', 'user10');

-- Inserting transaction history for user11
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (80.00, '2024-03-21 09:00:00', 'Buy', 7, 'IMPACT.CO', 'user11'),
    (85.00, '2024-03-21 11:30:00', 'Sell', 4, 'BLK', 'user11'),
    (75.00, '2024-03-21 13:45:00', 'Buy', 5, 'XOM', 'user11');
    
-- Inserting portfolio entry for user11
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (80.00, '2024-03-21 09:00:00', 'Buy', 7, 'IMPACT.CO', 'user11'),
    (85.00, '2024-03-21 11:30:00', 'Sell', 4, 'BLK', 'user11'),
    (75.00, '2024-03-21 13:45:00', 'Buy', 5, 'XOM', 'user11');

-- Inserting transaction history for user12
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 09:30:00', 'Buy', 12, 'NOVN.SW', 'user12'),
    (125.00, '2024-03-21 12:00:00', 'Sell', 6, 'MSCI', 'user12');
    
-- Inserting portfolio entry for user12
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 09:30:00', 'Buy', 12, 'NOVN.SW', 'user12'),
    (125.00, '2024-03-21 12:00:00', 'Sell', 6, 'MSCI', 'user12');

-- Inserting transaction history for user13
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (95.00, '2024-03-21 10:45:00', 'Buy', 8, 'KPMGY', 'user13'),
    (100.00, '2024-03-21 13:15:00', 'Sell', 4, 'EXK', 'user13'),
    (90.00, '2024-03-21 14:30:00', 'Buy', 6, 'PM', 'user13');
    
-- Inserting portfolio entry for user13
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (95.00, '2024-03-21 10:45:00', 'Buy', 8, 'KPMGY', 'user13'),
    (100.00, '2024-03-21 13:15:00', 'Sell', 4, 'EXK', 'user13'),
    (90.00, '2024-03-21 14:30:00', 'Buy', 6, 'PM', 'user13');

-- Inserting transaction history for user14
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (150.00, '2024-03-21 11:00:00', 'Buy', 10, 'UBP', 'user14'),
    (155.00, '2024-03-21 13:30:00', 'Sell', 5, 'MET', 'user14'),
    (145.00, '2024-03-21 14:45:00', 'Buy', 8, 'BCS', 'user14');

-- Inserting portfolio entry for user14
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (150.00, '2024-03-21 11:00:00', 'Buy', 10, 'UBP', 'user14'),
    (155.00, '2024-03-21 13:30:00', 'Sell', 5, 'MET', 'user14'),
    (145.00, '2024-03-21 14:45:00', 'Buy', 8, 'BCS', 'user14');

-- Inserting transaction history for user15
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (70.00, '2024-03-21 10:00:00', 'Buy', 6, 'AMZN', 'user15'),
    (75.00, '2024-03-21 12:30:00', 'Sell', 3, 'IMPACT.CO', 'user15'),
    (65.00, '2024-03-21 14:15:00', 'Buy', 5, 'BLK', 'user15');
    
-- Inserting portfolio entry for user15
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (70.00, '2024-03-21 10:00:00', 'Buy', 6, 'AMZN', 'user15'),
    (75.00, '2024-03-21 12:30:00', 'Sell', 3, 'IMPACT.CO', 'user15'),
    (65.00, '2024-03-21 14:15:00', 'Buy', 5, 'BLK', 'user15');

-- Inserting transaction history for user16
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (80.00, '2024-03-21 09:00:00', 'Buy', 7, 'XOM', 'user16'),
    (85.00, '2024-03-21 11:30:00', 'Sell', 4, 'NOVN.SW', 'user16'),
    (75.00, '2024-03-21 13:45:00', 'Buy', 5, 'KPMGY', 'user16');
    
-- Inserting portfolio entry for user16
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (80.00, '2024-03-21 09:00:00', 'Buy', 7, 'XOM', 'user16'),
    (85.00, '2024-03-21 11:30:00', 'Sell', 4, 'NOVN.SW', 'user16'),
    (75.00, '2024-03-21 13:45:00', 'Buy', 5, 'KPMGY', 'user16');

-- Inserting transaction history for user17
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 09:30:00', 'Buy', 12, 'EXK', 'user17'),
    (125.00, '2024-03-21 12:00:00', 'Sell', 6, 'PM', 'user17');
    
-- Inserting portfolio entry for user17
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (120.00, '2024-03-21 09:30:00', 'Buy', 12, 'EXK', 'user17'),
    (125.00, '2024-03-21 12:00:00', 'Sell', 6, 'PM', 'user17');

-- Inserting transaction history for user18
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (95.00, '2024-03-21 10:45:00', 'Buy', 8, 'UBP', 'user18'),
    (100.00, '2024-03-21 13:15:00', 'Sell', 4, 'MET', 'user18'),
    (90.00, '2024-03-21 14:30:00', 'Buy', 6, 'BCS', 'user18');
    
-- Inserting portfolio entry for user18
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (95.00, '2024-03-21 10:45:00', 'Buy', 8, 'UBP', 'user18'),
    (100.00, '2024-03-21 13:15:00', 'Sell', 4, 'MET', 'user18'),
    (90.00, '2024-03-21 14:30:00', 'Buy', 6, 'BCS', 'user18');

-- Inserting transaction history for user19
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (150.00, '2024-03-21 11:00:00', 'Buy', 10, 'AMZN', 'user19'),
    (155.00, '2024-03-21 13:30:00', 'Sell', 5, 'IMPACT.CO', 'user19'),
    (145.00, '2024-03-21 14:45:00', 'Buy', 8, 'BLK', 'user19');
    
-- Inserting portfolio entry for user19
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (150.00, '2024-03-21 11:00:00', 'Buy', 10, 'AMZN', 'user19'),
    (155.00, '2024-03-21 13:30:00', 'Sell', 5, 'IMPACT.CO', 'user19'),
    (145.00, '2024-03-21 14:45:00', 'Buy', 8, 'BLK', 'user19');

-- Inserting transaction history for user20
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (70.00, '2024-03-21 10:00:00', 'Buy', 6, 'XOM', 'user20'),
    (75.00, '2024-03-21 12:30:00', 'Sell', 3, 'NOVN.SW', 'user20'),
    (65.00, '2024-03-21 14:15:00', 'Buy', 5, 'KPMGY', 'user20');
    
-- Inserting portfolio entry for user20
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (70.00, '2024-03-21 10:00:00', 'Buy', 6, 'XOM', 'user20'),
    (75.00, '2024-03-21 12:30:00', 'Sell', 3, 'NOVN.SW', 'user20'),
    (65.00, '2024-03-21 14:15:00', 'Buy', 5, 'KPMGY', 'user20');

-- Inserting diverse transaction history data with dates before today
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (100.00, '2024-03-19 10:00:00', 'Buy', 10, 'CAAMX.SA', 'user1'),
    (110.00, '2024-03-20 11:30:00', 'Sell', 5, 'CSMF.PA', 'user1'),
    (90.00, '2024-03-18 13:45:00', 'Buy', 8, 'UBSG.SW', 'user1'),
    (50.00, '2024-03-19 09:30:00', 'Buy', 5, 'JEF', 'user2'),
    (55.00, '2024-03-20 14:00:00', 'Sell', 3, 'HNNMY', 'user2'),
    (120.00, '2024-03-18 10:45:00', 'Buy', 12, 'MSCI', 'user3'),
    (130.00, '2024-03-19 12:15:00', 'Sell', 7, 'KPMGY', 'user3'),
    (115.00, '2024-03-17 14:30:00', 'Buy', 10, 'EXK', 'user3'),
    (75.00, '2024-03-18 11:00:00', 'Buy', 8, 'PM', 'user4'),
    (200.00, '2024-03-20 10:30:00', 'Buy', 2, 'UBP', 'user5'),
    (190.00, '2024-03-17 12:00:00', 'Sell', 1, 'MET', 'user5');
    
-- Inserting diverse portfolio entry data with dates before today
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (100.00, '2024-03-19 10:00:00', 'Buy', 10, 'CAAMX.SA', 'user1'),
    (110.00, '2024-03-20 11:30:00', 'Sell', 5, 'CSMF.PA', 'user1'),
    (90.00, '2024-03-18 13:45:00', 'Buy', 8, 'UBSG.SW', 'user1'),
    (50.00, '2024-03-19 09:30:00', 'Buy', 5, 'JEF', 'user2'),
    (55.00, '2024-03-20 14:00:00', 'Sell', 3, 'HNNMY', 'user2'),
    (120.00, '2024-03-18 10:45:00', 'Buy', 12, 'MSCI', 'user3'),
    (130.00, '2024-03-19 12:15:00', 'Sell', 7, 'KPMGY', 'user3'),
    (115.00, '2024-03-17 14:30:00', 'Buy', 10, 'EXK', 'user3'),
    (75.00, '2024-03-18 11:00:00', 'Buy', 8, 'PM', 'user4'),
    (200.00, '2024-03-20 10:30:00', 'Buy', 2, 'UBP', 'user5'),
    (190.00, '2024-03-17 12:00:00', 'Sell', 1, 'MET', 'user5');

-- Inserting diverse portfolio entry data with dates spanning different months
INSERT INTO Portfolio_entry (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (100.00, '2023-12-15 10:00:00', 'Buy', 10, 'CAAMX.SA', 'user1'),
    (110.00, '2023-11-20 11:30:00', 'Sell', 5, 'CSMF.PA', 'user1'),
    (90.00, '2023-10-18 13:45:00', 'Buy', 8, 'UBSG.SW', 'user1'),
    (50.00, '2023-09-19 09:30:00', 'Buy', 5, 'JEF', 'user2'),
    (55.00, '2023-08-20 14:00:00', 'Sell', 3, 'HNNMY', 'user2'),
    (120.00, '2023-07-18 10:45:00', 'Buy', 12, 'MSCI', 'user3'),
    (130.00, '2023-06-19 12:15:00', 'Sell', 7, 'KPMGY', 'user3'),
    (115.00, '2023-05-17 14:30:00', 'Buy', 10, 'EXK', 'user3'),
    (75.00, '2023-04-18 11:00:00', 'Buy', 8, 'PM', 'user4'),
    (200.00, '2023-03-20 10:30:00', 'Buy', 2, 'UBP', 'user5'),
    (190.00, '2023-02-17 12:00:00', 'Sell', 1, 'MET', 'user5');

-- Inserting diverse transaction history data with dates spanning different months
INSERT INTO Transaction_history (price_quote, date, order_type, amount, Ticker, username)
VALUES
    (100.00, '2023-12-15 10:00:00', 'Buy', 10, 'CAAMX.SA', 'user1'),
    (110.00, '2023-11-20 11:30:00', 'Sell', 5, 'CSMF.PA', 'user1'),
    (90.00, '2023-10-18 13:45:00', 'Buy', 8, 'UBSG.SW', 'user1'),
    (50.00, '2023-09-19 09:30:00', 'Buy', 5, 'JEF', 'user2'),
    (55.00, '2023-08-20 14:00:00', 'Sell', 3, 'HNNMY', 'user2'),
    (120.00, '2023-07-18 10:45:00', 'Buy', 12, 'MSCI', 'user3'),
    (130.00, '2023-06-19 12:15:00', 'Sell', 7, 'KPMGY', 'user3'),
    (115.00, '2023-05-17 14:30:00', 'Buy', 10, 'EXK', 'user3'),
    (75.00, '2023-04-18 11:00:00', 'Buy', 8, 'PM', 'user4'),
    (200.00, '2023-03-20 10:30:00', 'Buy', 2, 'UBP', 'user5'),
    (190.00, '2023-02-17 12:00:00', 'Sell', 1, 'MET', 'user5');



CREATE INDEX createdAt ON Company (createdAt);
CREATE INDEX updatedAt ON Company (updatedAt);
CREATE INDEX currentScore ON Company (currentScore);
CREATE INDEX fundCategory ON Company (fundCategory);
CREATE INDEX fundCategory ON CompanySignup (fundCategory);
CREATE INDEX updatedAt ON PriceHistory (updatedAt);
CREATE INDEX updatedAt ON ScoreHistory (updatedAt);
CREATE INDEX age ON User (age);
CREATE INDEX country ON User (country);
CREATE INDEX gender ON User (gender);
CREATE INDEX date ON Transaction_history(date);
CREATE INDEX date ON Portfolio_entry(date);
