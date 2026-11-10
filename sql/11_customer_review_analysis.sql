SELECT
    COUNT(*) AS total_reviews,
    COUNT(DISTINCT order_id) AS reviewed_orders,

    ROUND(AVG(review_score), 2) AS average_review_score,

    SUM(CASE
        WHEN review_score IN (4, 5) THEN 1
        ELSE 0
    END) AS positive_reviews,

    SUM(CASE
        WHEN review_score = 3 THEN 1
        ELSE 0
    END) AS neutral_reviews,

    SUM(CASE
        WHEN review_score IN (1, 2) THEN 1
        ELSE 0
    END) AS negative_reviews,

    ROUND(
        100.0 * SUM(
            CASE WHEN review_score IN (4, 5) THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS positive_review_percentage,

    ROUND(
        100.0 * SUM(
            CASE WHEN review_score IN (1, 2) THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS negative_review_percentage

FROM reviews
WHERE review_score BETWEEN 1 AND 5;
