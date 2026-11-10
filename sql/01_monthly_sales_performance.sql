-- Monthly sales performance
-- Revenue definition: sum of product item prices.
-- Freight is reported separately.
-- Scope: delivered orders only.

WITH order_revenue AS (
    SELECT
        order_id,
        SUM(price) AS product_revenue,
        SUM(freight_value) AS freight_revenue
    FROM order_items
    GROUP BY order_id
)

SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS sales_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(r.product_revenue), 2) AS product_revenue,
    ROUND(SUM(r.freight_revenue), 2) AS freight_revenue,
    ROUND(
        SUM(r.product_revenue) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
INNER JOIN order_revenue r
    ON o.order_id = r.order_id
WHERE
    o.order_status = 'delivered'
    AND o.order_purchase_timestamp IS NOT NULL
GROUP BY
    strftime('%Y-%m', o.order_purchase_timestamp)
ORDER BY
    sales_month;
