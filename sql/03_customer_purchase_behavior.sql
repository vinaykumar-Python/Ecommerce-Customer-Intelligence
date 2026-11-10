-- Customer purchase behaviour
-- Scope: delivered orders only.
-- Customer identity: customer_unique_id.

WITH order_level AS (
    SELECT
        o.order_id,
        c.customer_unique_id,
        SUM(oi.price) AS product_revenue
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
        c.customer_unique_id
),

customer_level AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(product_revenue) AS total_product_revenue
    FROM order_level
    GROUP BY
        customer_unique_id
)

SELECT
    COUNT(*) AS total_unique_customers,

    SUM(
        CASE WHEN total_orders = 1
        THEN 1 ELSE 0 END
    ) AS one_time_customers,

    SUM(
        CASE WHEN total_orders > 1
        THEN 1 ELSE 0 END
    ) AS repeat_customers,

    ROUND(
        100.0 * SUM(
            CASE WHEN total_orders > 1
            THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS repeat_customer_rate_pct,

    ROUND(AVG(total_orders), 2) AS average_orders_per_customer,

    ROUND(SUM(total_product_revenue), 2) AS total_product_revenue

FROM customer_level;
