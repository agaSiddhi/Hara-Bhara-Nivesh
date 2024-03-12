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

INSERT INTO Industry (keyword, description) VALUES
('Capital Goods', 'Companies involved in manufacturing and distribution of industrial equipment and machinery.'),
('Financial', 'Financial institutions including banks, investment firms, and insurance companies.'),
('Services', 'Companies providing various types of services such as consulting, IT services, and hospitality.'),
('HealthCare', 'Companies involved in healthcare services, pharmaceuticals, and medical equipment manufacturing.'),
('Consumer Staples', 'Manufacturers and distributors of essential consumer goods like food, beverages, and household products.'),
('Other', 'Industries that do not fit into the defined categories or are niche markets.');

INSERT INTO Company (companyID, name, industryID, totalAssets, revenue, employeeCount, currentScore, foundedYear, fundCategory,wallet) VALUES
('AAPL', 'Apple Inc.', 1, 320000000000, 274515000000, 147000, 4.5, 1976, 'Equity',100),
('GOOGL', 'Alphabet Inc.', 1, 318000000000, 182527000000, 144056, 4.6, 1998, 'Equity',200),
('MSFT', 'Microsoft Corporation', 1, 278000000000, 168088000000, 181000, 4.4, 1975, 'Equity',150),
('AMZN', 'Amazon.com, Inc.', 3, 235000000000, 386064000000, 1298000, 4.5, 1994, 'Equity',300),
('JPM', 'JPMorgan Chase & Co.', 2, 2910000000000, 135229000000, 256981, 4.7, 2000, 'Debt',250),
('BRK.A', 'Berkshire Hathaway Inc.', 2, 894000000000, 327212000000, 391500,2.3, 1965, 'Hybrid',100), 
('FB', 'Facebook Inc.', 1, 155000000000, 104880000000, 60654, 4.6, 2004, 'Equity',220),
('NFLX', 'Netflix Inc.', 1, 38000000000, 25747000000, 9400, 4.2, 1997, 'Equity',200);

INSERT INTO CompanyWebsite (companyID, url) VALUES
('AAPL', 'https://www.apple.com'),
('GOOGL', 'https://www.google.com'),
('MSFT', 'https://www.microsoft.com'),
('AMZN', 'https://www.amazon.com'),
('JPM', 'https://www.jpmorganchase.com'),
('BRK.A', 'https://www.berkshirehathaway.com'),
('FB', 'https://www.facebook.com'),
('NFLX', 'https://www.netflix.com');

INSERT INTO Article (link, companyID) VALUES
('https://www.example.com/article1', 'AAPL'),
('https://www.example.com/article2', 'GOOGL'),
('https://www.example.com/article3', 'MSFT'),
('https://www.example.com/article4', 'AMZN'),
('https://www.example.com/article5', 'JPM'),
('https://www.example.com/article6', 'BRK.A'),
('https://www.example.com/article7', 'FB'),
('https://www.example.com/article8', 'NFLX');

-- Mock data for ScoreHistory table for AAPL (Apple Inc.)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'AAPL'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'AAPL'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'AAPL'), -- February 29th for leap year (2024 is a leap year)
(4.5, '2024-03-29', 'AAPL');

-- Mock data for ScoreHistory table for GOOGL (Gooogle Inc.)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'GOOGL'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'GOOGL'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'GOOGL'), -- February 29th for leap year (2024 is a leap year)
(4.6, '2024-03-29', 'GOOGL');

-- Mock data for ScoreHistory table for MSFT (Microsoft Corporation)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'MSFT'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'MSFT'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'MSFT'), -- February 29th for leap year (2024 is a leap year)
(4.4, '2024-03-29', 'MSFT');

-- Mock data for ScoreHistory table for AMZN (Amazon.com, Inc.)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'AMZN'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'AMZN'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'AMZN'), -- February 29th for leap year (2024 is a leap year)
(4.5, '2024-03-29', 'AMZN');

-- Mock data for ScoreHistory table for JPM (JPMorgan Chase & Co.)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'JPM'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'JPM'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'JPM'), -- February 29th for leap year (2024 is a leap year)
(4.7, '2024-03-29', 'JPM');

-- Mock data for ScoreHistory table for BRK.A (Berkshire Hathaway Inc.)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'BRK.A'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'BRK.A'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'BRK.A'), -- February 29th for leap year (2024 is a leap year)
(2.3, '2024-03-29', 'BRK.A');

-- Mock data for ScoreHistory table for FB (Facebook, Inc.)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'FB'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'FB'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'FB'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'FB'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'FB'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'FB'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'FB'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'FB'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'FB'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'FB'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'FB'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'FB'), -- February 29th for leap year (2024 is a leap year)
(4.6, '2024-03-29', 'FB');

-- Mock data for ScoreHistory table for NFLX (Netflix, Inc.)
INSERT INTO ScoreHistory (score, updatedAt, companyID)
VALUES
(ROUND(RAND() * 5, 2), '2022-05-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2022-06-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2022-07-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2022-08-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2022-09-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2022-10-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2022-11-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2022-12-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-01-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-02-28', 'NFLX'), -- February 28th for non-leap year
(ROUND(RAND() * 5, 2), '2023-03-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-04-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-05-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-06-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-07-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-08-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-09-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-10-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-11-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2023-12-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2024-01-29', 'NFLX'),
(ROUND(RAND() * 5, 2), '2024-02-29', 'NFLX'), -- February 29th for leap year (2024 is a leap year)
(4.2, '2024-03-29', 'NFLX');

-- Mock data for PriceHistory table for AAPL (Apple Inc.)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'AAPL'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'AAPL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'AAPL'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'AAPL');

-- Mock data for PriceHistory table for GOOGL (Alphabet Inc.)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'GOOGL'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'GOOGL'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'GOOGL'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'GOOGL');

-- Mock data for PriceHistory table for MSFT (Microsoft Corporation)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'MSFT'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'MSFT'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'MSFT'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'MSFT');

-- Mock data for PriceHistory table for AMZN (Amazon.com, Inc.)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'AMZN'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'AMZN'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'AMZN'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'AMZN');

-- Mock data for PriceHistory table for JPM (JPMorgan Chase & Co.)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'JPM'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'JPM'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'JPM'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'JPM');

-- Mock data for PriceHistory table for BRK.A (Berkshire Hathaway Inc.)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'BRK.A'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'BRK.A'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'BRK.A'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'BRK.A');

-- Mock data for PriceHistory table for FB (Facebook, Inc.)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'FB'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'FB'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'FB'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'FB');

-- Mock data for PriceHistory table for NFLX (Netflix, Inc.)
INSERT INTO PriceHistory (price, updatedAt, companyID)
VALUES
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-05-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-06-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-07-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-08-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-09-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-10-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-11-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2022-12-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-01-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-02-28', 'NFLX'), -- February 28th for non-leap year
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-03-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-04-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-05-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-06-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-07-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-08-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-09-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-10-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-11-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2023-12-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-01-29', 'NFLX'),
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-02-29', 'NFLX'), -- February 29th for leap year (2024 is a leap year)
(ROUND(RAND() * (500 - 100) + 100, 2), '2024-03-29', 'NFLX');

SELECT name,currentScore, (SELECT description FROM Industry WHERE Company.industryID = Industry.industryID)  FROM Company ORDER BY currentScore DESC;

SELECT c.companyID, c.name AS companyName, c.createdAt, c.updatedAt, c.totalAssets, c.revenue, c.employeeCount, c.currentScore, c.foundedYear, w.url
FROM Company c
LEFT JOIN CompanyWebsite w ON c.companyID = w.companyID
WHERE c.companyID = 1;
