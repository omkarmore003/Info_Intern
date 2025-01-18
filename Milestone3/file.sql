-- Create the database
CREATE DATABASE IF NOT EXISTS inventory_management;

-- Use the database
USE inventory_management;

-- Create the inventory table
CREATE TABLE IF NOT EXISTS inventory (
    country_name VARCHAR(255) PRIMARY KEY,
    product VARCHAR(255) ,
    stock_level INT,
    threshold INT
);

-- Insert mock data into the inventory table with 'coffee' as product for each entry
INSERT IGNORE INTO inventory (country_name, stock_level, threshold, product)
VALUES
    ('Bolivia', 500, 100, 'coffee'),
    ('Brazil', 1000, 200, 'coffee'),
    ('Cambodia', 400, 80, 'coffee'),
    ('China', 600, 120, 'coffee'),
    ('Colombia', 500, 100, 'coffee'),
    ('Ethiopia', 700, 180, 'coffee'),
    ('India', 1200, 250, 'coffee'),
    ('Indonesia', 900, 200, 'coffee'),
    ('Italy', 450, 90, 'coffee'),
    ('Kenya', 260, 50, 'coffee'),
    ('Korea', 300, 60, 'coffee'),
    ('Laos', 200, 40, 'coffee'),
    ('Malaysia', 350, 70, 'coffee'),
    ('Peru', 400, 80, 'coffee'),
    ('Russia', 500, 100, 'coffee'),
    ('Sri Lanka', 320, 65, 'coffee'),
    ('Thailand', 160, 30, 'coffee'),
    ('Uganda', 550, 110, 'coffee'),
    ('United States', 600, 120, 'coffee'),
    ('Vietnam', 800, 150, 'coffee');



drop database inventory_management;
