USE agentic_analytics;

-- ============================================================
-- 1. OVERALL BUSINESS KPIs
-- ============================================================

-- Total Orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- Total Customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- Total Revenue
SELECT ROUND(SUM(total_order_value), 2) AS total_revenue
FROM orders
WHERE order_status = 'delivered';

-- Average Order Value
SELECT ROUND(AVG(total_order_value), 2) AS average_order_value
FROM orders
WHERE order_status = 'delivered';


-- ============================================================
-- 2. MONTHLY REVENUE
-- ============================================================

SELECT
    order_year,
    order_month,
    order_month_name,
    ROUND(SUM(total_order_value), 2) AS revenue
FROM orders
WHERE order_status = 'delivered'
GROUP BY
    order_year,
    order_month,
    order_month_name
ORDER BY
    order_year,
    order_month;


-- ============================================================
-- 3. MONTHLY ORDER COUNT
-- ============================================================

SELECT
    order_year,
    order_month,
    COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY
    order_year,
    order_month
ORDER BY
    order_year,
    order_month;


-- ============================================================
-- 4. REVENUE BY CUSTOMER STATE
-- ============================================================

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_order_value), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY revenue DESC;


-- ============================================================
-- 5. TOP PRODUCT CATEGORIES
-- ============================================================

SELECT
    p.product_category,
    COUNT(DISTINCT oi.order_id) AS orders,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price), 2) AS product_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category
ORDER BY product_revenue DESC
LIMIT 10;


-- ============================================================
-- 6. TOP SELLERS
-- ============================================================

SELECT
    s.seller_id,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN sellers s
    ON oi.seller_id = s.seller_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY
    s.seller_id,
    s.seller_state
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 7. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    payment_type,
    COUNT(*) AS transactions,
    ROUND(SUM(payment_value), 2) AS payment_revenue,
    ROUND(AVG(payment_value), 2) AS average_payment
FROM payments
GROUP BY payment_type
ORDER BY payment_revenue DESC;


-- ============================================================
-- 8. REVIEW SCORE ANALYSIS
-- ============================================================

SELECT
    review_score,
    COUNT(*) AS review_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM reviews),
        2
    ) AS percentage
FROM reviews
GROUP BY review_score
ORDER BY review_score;


-- ============================================================
-- 9. DELIVERY PERFORMANCE
-- ============================================================

SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days,
    ROUND(AVG(delivery_delay_days), 2) AS average_delivery_delay_days,
    SUM(is_late) AS late_orders,
    COUNT(*) AS total_orders,
    ROUND(
        SUM(is_late) * 100.0 / COUNT(*),
        2
    ) AS late_order_percentage
FROM orders
WHERE order_status = 'delivered';


-- ============================================================
-- 10. ORDER STATUS ANALYSIS
-- ============================================================

SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


