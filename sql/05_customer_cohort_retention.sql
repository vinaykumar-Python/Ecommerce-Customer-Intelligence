WITH delivered_orders AS (
    SELECT DISTINCT
        c.customer_unique_id,
        o.order_id,
        strftime('%Y-%m', o.order_purchase_timestamp) AS purchase_month
    FROM orders o
    INNER JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp IS NOT NULL
),

customer_cohorts AS (
    SELECT
        customer_unique_id,
        MIN(purchase_month) AS cohort_month
    FROM delivered_orders
    GROUP BY customer_unique_id
),

customer_activity AS (
    SELECT DISTINCT
        d.customer_unique_id,
        c.cohort_month,
        d.purchase_month AS activity_month
    FROM delivered_orders d
    INNER JOIN customer_cohorts c
        ON d.customer_unique_id = c.customer_unique_id
),

cohort_periods AS (
    SELECT
        customer_unique_id,
        cohort_month,
        activity_month,
        (
            CAST(substr(activity_month, 1, 4) AS INTEGER)
            - CAST(substr(cohort_month, 1, 4) AS INTEGER)
        ) * 12
        +
        (
            CAST(substr(activity_month, 6, 2) AS INTEGER)
            - CAST(substr(cohort_month, 6, 2) AS INTEGER)
        ) AS cohort_index
    FROM customer_activity
),

cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(*) AS cohort_size
    FROM customer_cohorts
    GROUP BY cohort_month
),

cohort_retention AS (
    SELECT
        cohort_month,
        cohort_index,
        COUNT(DISTINCT customer_unique_id) AS active_customers
    FROM cohort_periods
    GROUP BY cohort_month, cohort_index
),

max_month AS (
    SELECT MAX(purchase_month) AS last_month
    FROM delivered_orders
),

cohort_grid AS (
    SELECT
        s.cohort_month,
        s.cohort_size,
        0 AS cohort_index,
        (
            CAST(substr(m.last_month, 1, 4) AS INTEGER)
            - CAST(substr(s.cohort_month, 1, 4) AS INTEGER)
        ) * 12
        +
        (
            CAST(substr(m.last_month, 6, 2) AS INTEGER)
            - CAST(substr(s.cohort_month, 6, 2) AS INTEGER)
        ) AS max_index
    FROM cohort_sizes s
    CROSS JOIN max_month m

    UNION ALL

    SELECT
        cohort_month,
        cohort_size,
        cohort_index + 1,
        max_index
    FROM cohort_grid
    WHERE cohort_index < max_index
)

SELECT
    g.cohort_month,
    g.cohort_index,
    g.cohort_size,
    COALESCE(r.active_customers, 0) AS active_customers,
    ROUND(
        100.0 * COALESCE(r.active_customers, 0) / g.cohort_size,
        2
    ) AS retention_rate
FROM cohort_grid g
LEFT JOIN cohort_retention r
    ON g.cohort_month = r.cohort_month
   AND g.cohort_index = r.cohort_index
ORDER BY
    g.cohort_month,
    g.cohort_index;
