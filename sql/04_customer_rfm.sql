-- Customer-level RFM dataset
-- Delivered orders only.
-- Identity: customer_unique_id.
-- Monetary: product item prices, excluding freight.

WITH order_level AS (
    SELECT
        o.order_id,
        c.customer_unique_id,
        o.order_purchase_timestamp,
        SUM(oi.price) AS order_revenue
    FROM orders o
    INNER JOIN customers c
        ON o.customer_id = c.customer_id
    INNER JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE
        o.order_status = 'delivered'
        AND o.order_purchase_timestamp IS NOT NULL
    GROUP BY
        o.order_id,
        c.customer_unique_id,
        o.order_purchase_timestamp
),

customer_rfm AS (
    SELECT
        customer_unique_id,
        MAX(order_purchase_timestamp) AS last_purchase_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(order_revenue) AS monetary
    FROM order_level
    GROUP BY customer_unique_id
),

reference_date AS (
    SELECT
        date(MAX(order_purchase_timestamp), '+1 day') AS analysis_date
    FROM order_level
)

SELECT
    cr.customer_unique_id,
    CAST(
        julianday(rd.analysis_date)
        - julianday(date(cr.last_purchase_date))
        AS INTEGER
    ) AS recency_days,
    cr.frequency,
    ROUND(cr.monetary, 2) AS monetary,
    date(cr.last_purchase_date) AS last_purchase_date,
    rd.analysis_date
FROM customer_rfm cr
CROSS JOIN reference_date rd
ORDER BY cr.monetary DESC;
