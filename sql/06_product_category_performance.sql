WITH delivered_order_items AS (
    SELECT
        oi.order_id,
        oi.product_id,
        oi.price,
        oi.freight_value,
        oi.order_item_id,
        o.customer_id
    FROM order_items oi
    INNER JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
),

category_performance AS (
    SELECT
        COALESCE(
            t.product_category_name_english,
            p.product_category_name,
            'Unknown'
        ) AS product_category,

        COUNT(DISTINCT d.order_id) AS total_orders,

        COUNT(DISTINCT d.customer_id) AS unique_customers,

        COUNT(d.order_item_id) AS units_sold,

        COUNT(DISTINCT d.product_id) AS distinct_products,

        ROUND(SUM(d.price), 2) AS product_revenue,

        ROUND(SUM(d.freight_value), 2) AS freight_revenue,

        ROUND(AVG(d.price), 2) AS average_item_price,

        ROUND(
            SUM(d.price) / COUNT(DISTINCT d.order_id),
            2
        ) AS revenue_per_order

    FROM delivered_order_items d

    INNER JOIN products p
        ON d.product_id = p.product_id

    LEFT JOIN category_translation t
        ON p.product_category_name = t.product_category_name

    GROUP BY
        COALESCE(
            t.product_category_name_english,
            p.product_category_name,
            'Unknown'
        )
)

SELECT *
FROM category_performance
ORDER BY product_revenue DESC;
