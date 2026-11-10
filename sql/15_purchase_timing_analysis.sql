WITH order_revenue AS (
    SELECT
        order_id,
        SUM(price) AS product_revenue
    FROM order_items
    GROUP BY order_id
),

purchase_data AS (
    SELECT
        o.order_id,
        CAST(strftime('%w', o.order_purchase_timestamp) AS INTEGER)
            AS weekday_number,
        CAST(strftime('%H', o.order_purchase_timestamp) AS INTEGER)
            AS purchase_hour,
        o.order_status,
        COALESCE(r.product_revenue, 0) AS product_revenue
    FROM orders o
    LEFT JOIN order_revenue r
        ON o.order_id = r.order_id
    WHERE o.order_purchase_timestamp IS NOT NULL
)

SELECT
    CASE weekday_number
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS purchase_weekday,

    weekday_number,
    purchase_hour,

    COUNT(DISTINCT order_id) AS total_orders,

    COUNT(DISTINCT CASE
        WHEN order_status = 'delivered'
        THEN order_id
    END) AS delivered_orders,

    COUNT(DISTINCT CASE
        WHEN order_status = 'canceled'
        THEN order_id
    END) AS canceled_orders,

    ROUND(SUM(CASE
        WHEN order_status = 'delivered'
        THEN product_revenue
        ELSE 0
    END), 2) AS delivered_product_revenue,

    ROUND(AVG(CASE
        WHEN order_status = 'delivered'
        THEN product_revenue
    END), 2) AS average_delivered_order_revenue

FROM purchase_data

GROUP BY weekday_number, purchase_hour
ORDER BY weekday_number, purchase_hour;
