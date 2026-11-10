SELECT
    c.customer_state,

    COUNT(DISTINCT o.order_id) AS total_orders,

    COUNT(DISTINCT CASE
        WHEN o.order_status = 'delivered'
        THEN o.order_id
    END) AS delivered_orders,

    COUNT(DISTINCT CASE
        WHEN o.order_status = 'canceled'
        THEN o.order_id
    END) AS canceled_orders,

    COUNT(DISTINCT CASE
        WHEN o.order_status = 'unavailable'
        THEN o.order_id
    END) AS unavailable_orders,

    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN o.order_status = 'canceled'
            THEN o.order_id
        END) / COUNT(DISTINCT o.order_id),
        2
    ) AS cancellation_rate,

    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN o.order_status IN ('canceled', 'unavailable')
            THEN o.order_id
        END) / COUNT(DISTINCT o.order_id),
        2
    ) AS unsuccessful_order_rate

FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id

GROUP BY c.customer_state
ORDER BY unsuccessful_order_rate DESC;
