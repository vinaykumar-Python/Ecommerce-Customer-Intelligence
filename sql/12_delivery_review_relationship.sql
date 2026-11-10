WITH review_per_order AS (
    SELECT
        order_id,
        AVG(review_score) AS average_order_review_score,
        COUNT(*) AS review_records
    FROM reviews
    WHERE review_score BETWEEN 1 AND 5
    GROUP BY order_id
),

delivery_details AS (
    SELECT
        o.order_id,
        r.average_order_review_score,
        r.review_records,

        CASE
            WHEN julianday(o.order_delivered_customer_date) >
                 julianday(o.order_estimated_delivery_date)
            THEN 'Late'
            ELSE 'On Time'
        END AS delivery_status

    FROM orders o
    INNER JOIN review_per_order r
        ON o.order_id = r.order_id

    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
)

SELECT
    delivery_status,
    COUNT(*) AS reviewed_orders,
    SUM(review_records) AS review_records,

    ROUND(AVG(average_order_review_score), 2)
        AS average_review_score,

    SUM(CASE
        WHEN average_order_review_score >= 4 THEN 1
        ELSE 0
    END) AS positive_orders,

    SUM(CASE
        WHEN average_order_review_score >= 3
         AND average_order_review_score < 4 THEN 1
        ELSE 0
    END) AS neutral_orders,

    SUM(CASE
        WHEN average_order_review_score < 3 THEN 1
        ELSE 0
    END) AS negative_orders,

    ROUND(
        100.0 * SUM(
            CASE WHEN average_order_review_score >= 4 THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS positive_order_percentage,

    ROUND(
        100.0 * SUM(
            CASE WHEN average_order_review_score < 3 THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS negative_order_percentage

FROM delivery_details
GROUP BY delivery_status
ORDER BY delivery_status;
