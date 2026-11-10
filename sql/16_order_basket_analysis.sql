WITH order_baskets AS (
    SELECT
        oi.order_id,
        COUNT(oi.order_item_id) AS total_items,
        COUNT(DISTINCT oi.product_id) AS distinct_products,
        SUM(oi.price) AS product_revenue,
        SUM(oi.freight_value) AS freight_value
    FROM order_items oi
    INNER JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY oi.order_id
),

classified_orders AS (
    SELECT
        *,
        CASE
            WHEN total_items = 1 THEN 'Single Item'
            WHEN total_items BETWEEN 2 AND 3 THEN '2-3 Items'
            ELSE '4+ Items'
        END AS basket_category
    FROM order_baskets
)

SELECT
    basket_category,

    COUNT(*) AS total_orders,

    SUM(total_items) AS total_units,

    ROUND(AVG(total_items), 2) AS average_items_per_order,

    ROUND(SUM(product_revenue), 2) AS total_product_revenue,

    ROUND(AVG(product_revenue), 2) AS average_order_value,

    ROUND(SUM(freight_value), 2) AS total_freight,

    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS order_percentage

FROM classified_orders

GROUP BY basket_category

ORDER BY
    CASE basket_category
        WHEN 'Single Item' THEN 1
        WHEN '2-3 Items' THEN 2
        ELSE 3
    END;
