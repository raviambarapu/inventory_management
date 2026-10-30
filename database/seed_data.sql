INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic gadgets and accessories'),
('Stationery', 'Office and school supplies'),
('Furniture', 'Office and home furniture');

INSERT INTO suppliers (supplier_name, contact_email, phone, address) VALUES
('TechSource Pvt Ltd', 'sales@techsource.com', '9876543210', 'Hyderabad, India'),
('OfficeMart', 'contact@officemart.com', '9123456780', 'Chennai, India'),
('FurniCraft', 'info@furnicraft.com', '9000011122', 'Bengaluru, India');

INSERT INTO customers (customer_name, email, phone, address) VALUES
('Ravi Ambarapu', 'ravi@example.com', '9998887776', 'Andhra Pradesh, India'),
('Sneha Reddy', 'sneha@example.com', '9887766554', 'Vijayawada, India'),
('Arjun Kumar', 'arjun@example.com', '9776655443', 'Vizag, India');

INSERT INTO products (product_name, category_id, supplier_id, unit_price, quantity_in_stock, reorder_level) VALUES
('Wireless Mouse', 1, 1, 499.00, 50, 10),
('USB-C Hub', 1, 1, 1299.00, 30, 5),
('A4 Notebook', 2, 2, 60.00, 200, 20),
('Ballpoint Pen (Pack of 10)', 2, 2, 90.00, 150, 20),
('Office Chair', 3, 3, 4999.00, 15, 3),
('Study Table', 3, 3, 3499.00, 10, 2);