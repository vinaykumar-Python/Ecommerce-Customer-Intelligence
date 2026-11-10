WITH review_per_order AS (
    SELECT
        order_id,
        AVG(review_score) AS average_review_score
    FROM reviews
    WHERE review_score BETWEEN 1 AND 5
    GROUP BY order_id
),

order_categories AS (
    SELECT DISTINCT
        oi.order_id,
        COALESCE(
            t.product_category_name_english,
            p.product_category_name,
            'Unknown'
        ) AS category_name
    FROM order_items oi
    INNER JOIN products p
        ON oi.product_id = p.product_id
    LEFT JOIN category_translation t
        ON p.product_category_name = t.product_category_name
),

category_reviews AS (
    SELECT
        oc.category_name,
        r.order_id,
        r.average_review_score
    FROM order_categories oc
    INNER JOIN review_per_order r
        ON oc.order_id = r.order_id
)

SELECT
    category_name,
    COUNT(DISTINCT order_id) AS reviewed_orders,

    ROUND(AVG(average_review_score), 2)
        AS average_review_score,

    SUM(CASE
        WHEN average_review_score >= 4 THEN 1
        ELSE 0
    END) AS positive_orders,

    SUM(CASE
        WHEN average_review_score >= 3
         AND average_review_score < 4 THEN 1
        ELSE 0
    END) AS neutral_orders,

    SUM(CASE
        WHEN average_review_score < 3 THEN 1
        ELSE 0
    END) AS negative_orders,

    ROUND(
        100.0 * SUM(
            CASE WHEN average_review_score < 3 THEN 1 ELSE 0 END
        ) / COUNT(DISTINCT order_id),
        2
    ) AS negative_review_percentage

FROM category_reviews
GROUP BY category_name
ORDER BY average_review_score ASC;
