-- =========================================================
-- AGENTIC BUSINESS ANALYTICS
-- MySQL Database Schema
-- =========================================================

CREATE DATABASE IF NOT EXISTS agentic_analytics;

USE agentic_analytics;


-- =========================================================
-- 1. CUSTOMERS
-- =========================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);


-- =========================================================
-- 2. PRODUCTS
-- =========================================================

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(150),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2),
    product_category_name_english VARCHAR(150),
    product_category VARCHAR(150)
);


-- =========================================================
-- 3. SELLERS
-- =========================================================

CREATE TABLE IF NOT EXISTS sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);


-- =========================================================
-- 4. ORDERS
-- =========================================================

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,

    customer_id VARCHAR(50),

    order_status VARCHAR(30),

    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,

    delivery_days DECIMAL(10,2),
    delivery_delay_days DECIMAL(10,2),

    is_late BOOLEAN,

    product_revenue DECIMAL(12,2),
    freight_cost DECIMAL(12,2),

    total_items INT,

    total_order_value DECIMAL(12,2),

    order_year INT,
    order_month INT,
    order_month_name VARCHAR(20),
    order_quarter INT,
    order_day INT,
    order_day_of_week VARCHAR(20),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- =========================================================
-- 5. ORDER ITEMS
-- =========================================================

CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR(50),
    order_item_id INT,

    product_id VARCHAR(50),
    seller_id VARCHAR(50),

    shipping_limit_date DATETIME,

    price DECIMAL(12,2),
    freight_value DECIMAL(12,2),

    PRIMARY KEY (order_id, order_item_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)
);


-- =========================================================
-- 6. PAYMENTS
-- =========================================================

CREATE TABLE IF NOT EXISTS payments (
    order_id VARCHAR(50),
    payment_sequential INT,

    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value DECIMAL(12,2),

    PRIMARY KEY (order_id, payment_sequential),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =========================================================
-- 7. REVIEWS
-- =========================================================

CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(50) PRIMARY KEY,

    order_id VARCHAR(50),

    review_score INT,

    review_comment_title TEXT,
    review_comment_message TEXT,

    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =========================================================
-- 8. GEOLOCATION
-- =========================================================

CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix INT,

    geolocation_lat DECIMAL(12,8),
    geolocation_lng DECIMAL(12,8),

    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(10)
);


-- =========================================================
-- 9. CATEGORY TRANSLATION
-- =========================================================

CREATE TABLE IF NOT EXISTS category_translation (
    product_category_name VARCHAR(150),
    product_category_name_english VARCHAR(150)
);


-- =========================================================
-- DATABASE SETUP COMPLETE
-- =========================================================