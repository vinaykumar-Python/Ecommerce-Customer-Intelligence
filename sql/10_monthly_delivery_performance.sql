WITH delivery_details AS (
    SELECT
        order_id,
        strftime('%Y-%m', order_purchase_timestamp) AS purchase_month,

        julianday(order_delivered_customer_date) -
        julianday(order_purchase_timestamp) AS actual_delivery_days,

        julianday(order_delivered_customer_date) -
        julianday(order_estimated_delivery_date) AS delay_days

    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
)

SELECT
    purchase_month,
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
GROUP BY purchase_month
ORDER BY purchase_month;
