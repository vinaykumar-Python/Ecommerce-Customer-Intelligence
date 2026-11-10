WITH seller_order_items AS (
    SELECT
        oi.seller_id,
        oi.order_id,
        oi.product_id,
        oi.order_item_id,
        oi.price,
        oi.freight_value,
        c.customer_unique_id
    FROM order_items oi
    INNER JOIN orders o
        ON oi.order_id = o.order_id
    INNER JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
),
seller_performance AS (
    SELECT
        s.seller_id,
        s.seller_state,
        s.seller_city,
        COUNT(DISTINCT d.order_id) AS total_orders,
        COUNT(DISTINCT d.customer_unique_id) AS unique_customers,
        COUNT(d.order_item_id) AS units_sold,
        COUNT(DISTINCT d.product_id) AS distinct_products,
        ROUND(SUM(d.price), 2) AS product_revenue,
        ROUND(SUM(d.freight_value), 2) AS freight_revenue,
        ROUND(AVG(d.price), 2) AS average_item_price,
        ROUND(
            SUM(d.price) / COUNT(DISTINCT d.order_id), 2
        ) AS revenue_per_order
    FROM seller_order_items d
    INNER JOIN sellers s
        ON d.seller_id = s.seller_id
    GROUP BY
        s.seller_id,
        s.seller_state,
        s.seller_city
)
SELECT *
FROM seller_performance
ORDER BY product_revenue DESC;
