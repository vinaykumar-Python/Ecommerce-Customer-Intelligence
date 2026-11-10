WITH delivery_details AS (
    SELECT
        order_id,
        julianday(order_delivered_customer_date) -
        julianday(order_purchase_timestamp) AS actual_delivery_days,

        julianday(order_estimated_delivery_date) -
        julianday(order_purchase_timestamp) AS estimated_delivery_days,

        julianday(order_delivered_customer_date) -
        julianday(order_estimated_delivery_date) AS delay_days

    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
),

classified_orders AS (
    SELECT *,
        CASE
            WHEN delay_days <= 0 THEN 'On Time'
            ELSE 'Late'
        END AS delivery_status
    FROM delivery_details
)

SELECT
    COUNT(*) AS total_delivered_orders,

    ROUND(AVG(actual_delivery_days), 2)
        AS average_actual_delivery_days,

    ROUND(AVG(estimated_delivery_days), 2)
        AS average_estimated_delivery_days,

    ROUND(AVG(delay_days), 2)
        AS average_delay_days,

    SUM(CASE WHEN delivery_status = 'On Time' THEN 1 ELSE 0 END)
        AS on_time_orders,

    SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END)
        AS late_orders,

    ROUND(
        100.0 * SUM(CASE WHEN delivery_status = 'On Time' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS on_time_delivery_percentage,

    ROUND(
        100.0 * SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS late_delivery_percentage

FROM classified_orders;
