USE crm_db;
INSERT INTO customers(name,email,phone,address) VALUES
('Ravi Kumar','ravi@example.com','9876543210','Chirala'),
('Anita Sharma','anita@example.com','9876501234','Hyderabad'),
('Kiran Reddy','kiran@example.com','9123456780','Vijayawada');
INSERT INTO products(product_name,price,stock) VALUES
('Laptop',65000,10),('Wireless Mouse',1200,50),('Keyboard',1800,30);
INSERT INTO employees(employee_name,department) VALUES
('Arun Kumar','Sales'),('Priya Rao','Support');
INSERT INTO orders(customer_id,employee_id,order_date,total_amount) VALUES
(1,1,'2026-09-01',66200),(2,1,'2026-09-03',1800),(3,2,'2026-09-05',1200);
INSERT INTO transactions(order_id,amount,payment_status) VALUES
(1,66200,'Paid'),(2,1800,'Pending'),(3,1200,'Paid');
