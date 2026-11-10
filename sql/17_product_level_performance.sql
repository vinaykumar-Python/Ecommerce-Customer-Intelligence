WITH product_sales AS (
    SELECT
        oi.product_id,
        COALESCE(
            ct.product_category_name_english,
            p.product_category_name,
            'Unknown'
        ) AS product_category,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        COUNT(*) AS units_sold,
        COUNT(DISTINCT oi.seller_id) AS unique_sellers,
        SUM(oi.price) AS product_revenue,
        SUM(oi.freight_value) AS freight_revenue,
        AVG(oi.price) AS average_item_price
    FROM order_items oi
    INNER JOIN orders o
        ON oi.order_id = o.order_id
    LEFT JOIN products p
        ON oi.product_id = p.product_id
    LEFT JOIN category_translation ct
        ON p.product_category_name = ct.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY
        oi.product_id,
        COALESCE(
            ct.product_category_name_english,
            p.product_category_name,
            'Unknown'
        )
),
ranked_products AS (
    SELECT
        *,
        SUM(product_revenue) OVER () AS total_revenue,
        RANK() OVER (
            ORDER BY product_revenue DESC
        ) AS revenue_rank,
        SUM(product_revenue) OVER (
            ORDER BY product_revenue DESC, product_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue
    FROM product_sales
)
SELECT
    product_id,
    product_category,
    total_orders,
    units_sold,
    unique_sellers,
    ROUND(product_revenue, 2) AS product_revenue,
    ROUND(freight_revenue, 2) AS freight_revenue,
    ROUND(average_item_price, 2) AS average_item_price,
    revenue_rank,
    ROUND(
        product_revenue * 100.0 / total_revenue,
        2
    ) AS revenue_share_percentage,
    ROUND(
        cumulative_revenue * 100.0 / total_revenue,
        2
    ) AS cumulative_revenue_share_percentage
FROM ranked_products
ORDER BY product_revenue DESC, product_id;
