USE agentic_analytics;

-- ============================================================
-- 1. MONTHLY SALES VIEW
-- ============================================================

CREATE OR REPLACE VIEW monthly_sales_view AS
SELECT
    order_year,
    order_month,
    order_month_name,
    ROUND(SUM(total_order_value), 2) AS revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(total_order_value), 2) AS average_order_value
FROM orders
WHERE order_status = 'delivered'
GROUP BY
    order_year,
    order_month,
    order_month_name;


-- ============================================================
-- 2. CUSTOMER SALES VIEW
-- ============================================================

CREATE OR REPLACE VIEW customer_sales_view AS
SELECT
    c.customer_unique_id,
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_order_value), 2) AS total_spent,
    ROUND(AVG(o.total_order_value), 2) AS average_order_value,
    MAX(o.order_purchase_timestamp) AS last_order_date
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'delivered'
GROUP BY
    c.customer_unique_id,
    c.customer_state;


-- ============================================================
-- 3. PRODUCT CATEGORY PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW category_performance_view AS
SELECT
    p.product_category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(AVG(oi.price), 2) AS average_item_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY
    p.product_category;


-- ============================================================
-- 4. SELLER PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW seller_performance_view AS
SELECT
    s.seller_id,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(SUM(oi.freight_value), 2) AS freight_revenue
FROM order_items oi
JOIN sellers s
    ON oi.seller_id = s.seller_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY
    s.seller_id,
    s.seller_state;


-- ============================================================
-- 5. DELIVERY PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW delivery_performance_view AS
SELECT
    order_year,
    order_month,
    COUNT(*) AS total_delivered_orders,
    ROUND(AVG(delivery_days), 2) AS average_delivery_days,
    ROUND(AVG(delivery_delay_days), 2) AS average_delivery_delay_days,
    SUM(is_late) AS late_orders,
    ROUND(
        SUM(is_late) * 100.0 / COUNT(*),
        2
    ) AS late_order_percentage
FROM orders
WHERE order_status = 'delivered'
GROUP BY
    order_year,
    order_month;


-- ============================================================
-- 6. PAYMENT PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW payment_performance_view AS
SELECT
    payment_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS average_payment_value
FROM payments
GROUP BY payment_type;


-- ============================================================
-- 7. REVIEW PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW review_performance_view AS
SELECT
    review_score,
    COUNT(*) AS review_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM reviews),
        2
    ) AS review_percentage
FROM reviews
GROUP BY review_score;


-- ============================================================
-- 8. POWER BI ORDER ANALYTICS VIEW
-- ============================================================

CREATE OR REPLACE VIEW powerbi_order_analytics AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_state,

    o.order_status,

    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    o.order_year,
    o.order_month,
    o.order_month_name,
    o.order_quarter,
    o.order_day_of_week,

    o.product_revenue,
    o.freight_cost,
    o.total_order_value,
    o.total_items,

    o.delivery_days,
    o.delivery_delay_days,
    o.is_late

FROM orders o

LEFT JOIN customers c
    ON o.customer_id = c.customer_id;