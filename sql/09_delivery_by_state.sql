WITH delivery_details AS (
    SELECT
        o.order_id,
        c.customer_state,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date,

        julianday(o.order_delivered_customer_date) -
        julianday(o.order_purchase_timestamp) AS actual_delivery_days,

        julianday(o.order_delivered_customer_date) -
        julianday(o.order_estimated_delivery_date) AS delay_days

    FROM orders o
    INNER JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
)

SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(AVG(actual_delivery_days), 2)
        AS average_delivery_days,

    ROUND(AVG(delay_days), 2)
        AS average_delay_days,

    SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END)
        AS late_orders,

    SUM(CASE WHEN delay_days <= 0 THEN 1 ELSE 0 END)
        AS on_time_orders,

    ROUND(
        100.0 * SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END)
        / COUNT(DISTINCT order_id),
        2
    ) AS late_delivery_percentage

FROM delivery_details

GROUP BY customer_state

ORDER BY late_delivery_percentage DESC;
