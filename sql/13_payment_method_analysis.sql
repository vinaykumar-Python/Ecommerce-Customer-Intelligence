WITH order_payment_method AS (
    SELECT
        p.order_id,
        p.payment_type,
        SUM(p.payment_value) AS order_payment_value,
        MAX(p.payment_installments) AS payment_installments
    FROM payments p
    INNER JOIN orders o
        ON p.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY
        p.order_id,
        p.payment_type
)

SELECT
    payment_type,

    COUNT(*) AS order_payment_count,

    ROUND(SUM(order_payment_value), 2)
        AS total_payment_value,

    ROUND(AVG(order_payment_value), 2)
        AS average_payment_value,

    ROUND(AVG(payment_installments), 2)
        AS average_installments,

    MAX(payment_installments)
        AS maximum_installments,

    ROUND(
        100.0 * SUM(order_payment_value) /
        SUM(SUM(order_payment_value)) OVER (),
        2
    ) AS payment_value_percentage

FROM order_payment_method

GROUP BY payment_type

ORDER BY total_payment_value DESC;
