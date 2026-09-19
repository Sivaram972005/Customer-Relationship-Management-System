CREATE DATABASE IF NOT EXISTS crm_db;
USE crm_db;
DROP VIEW IF EXISTS customer_orders;
DROP TRIGGER IF EXISTS after_transaction_insert;
DROP PROCEDURE IF EXISTS GetCustomerOrders;
DROP TABLE IF EXISTS transaction_audit;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
 customer_id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(120) NOT NULL UNIQUE,
 phone VARCHAR(20), address VARCHAR(255),
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE products (
 product_id INT AUTO_INCREMENT PRIMARY KEY,
 product_name VARCHAR(120) NOT NULL,
 price DECIMAL(12,2) NOT NULL,
 stock INT NOT NULL DEFAULT 0
);
CREATE TABLE employees (
 employee_id INT AUTO_INCREMENT PRIMARY KEY,
 employee_name VARCHAR(100) NOT NULL,
 department VARCHAR(100) NOT NULL
);
CREATE TABLE orders (
 order_id INT AUTO_INCREMENT PRIMARY KEY,
 customer_id INT NOT NULL,
 employee_id INT,
 order_date DATE NOT NULL,
 total_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
 FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
 FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
);
CREATE TABLE transactions (
 transaction_id INT AUTO_INCREMENT PRIMARY KEY,
 order_id INT NOT NULL,
 amount DECIMAL(12,2) NOT NULL,
 payment_status ENUM('Pending','Paid','Failed','Refunded') DEFAULT 'Pending',
 transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(order_id) REFERENCES orders(order_id)
);
CREATE TABLE transaction_audit (
 audit_id INT AUTO_INCREMENT PRIMARY KEY,
 transaction_id INT NOT NULL,
 action_type VARCHAR(30) NOT NULL,
 audit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE VIEW customer_orders AS
SELECT c.customer_id,c.name AS customer_name,c.email,o.order_id,o.order_date,o.total_amount,e.employee_name
FROM customers c JOIN orders o ON c.customer_id=o.customer_id
LEFT JOIN employees e ON o.employee_id=e.employee_id;
DELIMITER //
CREATE PROCEDURE GetCustomerOrders(IN cid INT)
BEGIN
 SELECT o.order_id,o.order_date,o.total_amount,e.employee_name
 FROM orders o LEFT JOIN employees e ON o.employee_id=e.employee_id
 WHERE o.customer_id=cid ORDER BY o.order_date DESC;
END //
CREATE TRIGGER after_transaction_insert AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
 INSERT INTO transaction_audit(transaction_id,action_type) VALUES(NEW.transaction_id,'INSERT');
END //
DELIMITER ;
