-- Create a MySQL database connection
CREATE DATABASE IF NOT EXISTS dbms;
USE dbms;

CREATE TABLE IF NOT EXISTS amc_rec (
    amc_id INT NOT NULL PRIMARY KEY,
    amc_name VARCHAR(255),
    address VARCHAR(255),
    amc_type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS asset (
    asset_id INT NOT NULL PRIMARY KEY,
    asset_type VARCHAR(255),
    asset_name VARCHAR(255),
    no_of_shares INT,
    promoter_holding VARCHAR(255),
    valuation VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS bank (
    ifsc_code VARCHAR(20),
    bank_name VARCHAR(255),
    account_no INT NOT NULL PRIMARY KEY,
    balance_amount DECIMAL(10, 2),
    amc_id INT,
    FOREIGN KEY (amc_id) REFERENCES amc_rec(amc_id)
);

CREATE TABLE IF NOT EXISTS certificate (
    cert_id INT NOT NULL PRIMARY KEY,
    cert_name VARCHAR(255),
    issue_date DATE,
    expiry_date DATE
);

CREATE TABLE IF NOT EXISTS cus (
    cus_id INT NOT NULL PRIMARY KEY,
    cus_dob DATE,
    cus_type VARCHAR(255),
    cus_name VARCHAR(255),
    cus_addr VARCHAR(255),
    cus_g VARCHAR(1),
    cus_ph CHAR(10),
    cus_age INT,
    amc_id INT,
    FOREIGN KEY (amc_id) REFERENCES amc_rec(amc_id)
);

CREATE TABLE IF NOT EXISTS fund_manager (
    fm_id INT NOT NULL PRIMARY KEY,
    amc_id INT,
    FOREIGN KEY (amc_id) REFERENCES amc_rec(amc_id)
);

CREATE TABLE IF NOT EXISTS fund (
    fund_id INT NOT NULL PRIMARY KEY,
    asset_class VARCHAR(255),
    fund_size INT,
    return_pa INT,
    fund_balance INT,
    manages_id INT,
    FOREIGN KEY (manages_id) REFERENCES fund_manager(fm_id)
);

CREATE TABLE IF NOT EXISTS investment (
    inv_id INT NOT NULL PRIMARY KEY,
    invest_amt INT,
    fund_id INT,
    cus_id INT,
    invest_date DATE,
    FOREIGN KEY (fund_id) REFERENCES fund(fund_id),
    FOREIGN KEY (cus_id) REFERENCES cus(cus_id)
);

CREATE TABLE IF NOT EXISTS transaction (
    transaction_id INT NOT NULL PRIMARY KEY,
    timestamp DATETIME,
    transaction_amount INT,
    transaction_type VARCHAR(255),
    asset_id INT,
    FOREIGN KEY (asset_id) REFERENCES asset(asset_id)
);

-- Create a trigger to update fund balance after each investment
DELIMITER //
CREATE TRIGGER update_fund_balance AFTER INSERT ON investment
FOR EACH ROW
BEGIN
    UPDATE fund
    SET fund_balance = fund_balance - NEW.invest_amt
    WHERE fund_id = NEW.fund_id;
END;
//
DELIMITER ;

-- Create a trigger to log transactions
DELIMITER //
CREATE TRIGGER log_transaction AFTER INSERT ON transaction
FOR EACH ROW
BEGIN
    INSERT INTO transaction_log (transaction_id, timestamp, transaction_type, asset_id)
    VALUES (NEW.transaction_id, NEW.timestamp, NEW.transaction_type, NEW.asset_id);
END;
//
DELIMITER ;


SELECT
    cus_id,
    cus_name,
    (
        SELECT MAX(invest_amt) FROM investment WHERE investment.cus_id = cus.cus_id
    ) AS total_investment
FROM cus;

-- Stored procedure to add a certificate to the database
DELIMITER //
CREATE PROCEDURE addcert(
    IN cert_id_param INT,
    IN cert_name_param VARCHAR(255),
    IN issue_date_param DATE,
    IN expiry_date_param DATE
)
BEGIN
    INSERT INTO certificate (cert_id, cert_name, issue_date, expiry_date)
    VALUES (cert_id_param, cert_name_param, issue_date_param, expiry_date_param);
END;
//
DELIMITER ;

-- Query to retrieve fund information for a specific asset management company (AMC)
SELECT
    f.fund_id,
    f.asset_class,
    f.fund_size,
    f.return_pa,
    f.fund_balance
FROM fund AS f
JOIN fund_manager AS fm ON f.manages_id = fm.fm_id
WHERE fm.amc_id = %s;

-- Query to insert investment details into the investment table
INSERT INTO investment (inv_id, invest_date, invest_amt, fund_id, cus_id)
VALUES (%s, %s, %s, %s, %s);

-- Query to calculate the total investment amount for a specific customer
SELECT SUM(invest_amt) FROM investment WHERE cus_id = %s;

-- Query to create a user with specified privileges
CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';

-- Query to grant privileges to a user
GRANT {privileges} ON your_database.* TO '{username}'@'localhost';

-- Query to flush privileges to apply changes
FLUSH PRIVILEGES;

-- Query to create a new fund manager and insert it into the fund_manager table
INSERT INTO fund_manager (fm_id, amc_id) VALUES (%s, %s);

-- Query to insert fund details into the fund table
INSERT INTO fund (fund_id, asset_class, fund_size, return_pa, fund_balance, manages_id)
VALUES (%s, %s, %s, %s, %s, %s);

-- Inserting a new customer record into the 'cus' table
INSERT INTO cus (cus_id, cus_dob, cus_type, cus_name, cus_addr, cus_g, cus_ph, cus_age, amc_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);

-- Checking if a customer record already exists
SELECT * FROM cus WHERE cus_id = %s;
-- Searching for a bank account by account number in the 'bank' table
SELECT * FROM bank WHERE account_no = %s;

-- Retrieving all bank accounts associated with a specific AMC from the 'bank' table
SELECT * FROM bank WHERE amc_id = %s;

-- Inserting a new bank account record into the 'bank' table
INSERT INTO bank (ifsc_code, bank_name, account_no, balance_amount, amc_id)
VALUES (%s, %s, %s, %s, %s);


-- Change user password
SET PASSWORD FOR '{username}'@'localhost' = PASSWORD('{new_password}');

-- Update customer address
UPDATE cus SET cus_addr = %s WHERE cus_id = %s;

-- Delete a customer account
DELETE FROM cus WHERE cus_id = %s;

-- Drop a user
DROP USER '{username}'@'localhost';

-- Drop a trigger
DROP TRIGGER IF EXISTS update_fund_balance;
DROP TRIGGER IF EXISTS log_transaction;

-- Drop a stored procedure
DROP PROCEDURE IF EXISTS addcert;

-- Drop a table
DROP TABLE IF EXISTS transaction_log;




