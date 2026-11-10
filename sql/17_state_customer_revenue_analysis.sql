WITH order_revenue AS (
    SELECT
        order_id,
        SUM(price) AS product_revenue
    FROM order_items
    GROUP BY order_id
),

customer_orders AS (
    SELECT
        c.customer_state,
        c.customer_unique_id,
        o.order_id,
        COALESCE(r.product_revenue, 0) AS product_revenue
    FROM orders o
    INNER JOIN customers c
        ON o.customer_id = c.customer_id
    LEFT JOIN order_revenue r
        ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
),

customer_state_summary AS (
    SELECT
        customer_state,
        customer_unique_id,
        COUNT(DISTINCT order_id) AS customer_orders,
        SUM(product_revenue) AS customer_revenue
    FROM customer_orders
    GROUP BY customer_state, customer_unique_id
)

SELECT
    customer_state,

    COUNT(*) AS unique_customers,

    SUM(customer_orders) AS delivered_orders,

    SUM(CASE
        WHEN customer_orders > 1 THEN 1
        ELSE 0
    END) AS repeat_customers,

    ROUND(
        100.0 * SUM(CASE
            WHEN customer_orders > 1 THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS repeat_customer_percentage,

    ROUND(SUM(customer_revenue), 2) AS product_revenue,

    ROUND(
        SUM(customer_revenue) / SUM(customer_orders),
        2
    ) AS average_order_value,

    ROUND(
        100.0 * SUM(customer_revenue) /
        SUM(SUM(customer_revenue)) OVER (),
        2
    ) AS revenue_share_percentage

FROM customer_state_summary

GROUP BY customer_state
ORDER BY product_revenue DESC;
