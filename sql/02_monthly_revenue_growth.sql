WITH RECURSIVE

-- 1. Calculate monthly sales from delivered orders.
monthly_sales AS (
    SELECT
        strftime('%Y-%m', o.order_purchase_timestamp) AS sales_month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.price) AS product_revenue,
        SUM(oi.freight_value) AS freight_revenue
    FROM orders o
    INNER JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE
        o.order_status = 'delivered'
        AND o.order_purchase_timestamp IS NOT NULL
    GROUP BY
        strftime('%Y-%m', o.order_purchase_timestamp)
),

-- 2. Generate every calendar month in the dataset's sales period.
calendar_months(month_start) AS (
    SELECT
        date(MIN(order_purchase_timestamp), 'start of month')
    FROM orders
    WHERE
        order_status = 'delivered'
        AND order_purchase_timestamp IS NOT NULL

    UNION ALL

    SELECT
        date(month_start, '+1 month')
    FROM calendar_months
    WHERE month_start < (
        SELECT date(MAX(order_purchase_timestamp), 'start of month')
        FROM orders
        WHERE
            order_status = 'delivered'
            AND order_purchase_timestamp IS NOT NULL
    )
),

-- 3. Fill months without delivered sales with zero.
complete_monthly_sales AS (
    SELECT
        strftime('%Y-%m', c.month_start) AS sales_month,
        COALESCE(m.total_orders, 0) AS total_orders,
        COALESCE(m.product_revenue, 0) AS product_revenue,
        COALESCE(m.freight_revenue, 0) AS freight_revenue
    FROM calendar_months c
    LEFT JOIN monthly_sales m
        ON strftime('%Y-%m', c.month_start) = m.sales_month
),

-- 4. Retrieve the previous calendar month's figures.
sales_with_previous AS (
    SELECT
        *,
        LAG(sales_month) OVER (
            ORDER BY sales_month
        ) AS previous_month,

        LAG(product_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_month_revenue

    FROM complete_monthly_sales
)

-- 5. Calculate month-over-month revenue growth.
SELECT
    sales_month,
    total_orders,
    ROUND(product_revenue, 2) AS product_revenue,
    previous_month,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,

    CASE
        WHEN previous_month_revenue > 0
        THEN ROUND(
            (
                (product_revenue - previous_month_revenue)
                / previous_month_revenue
            ) * 100,
            2
        )
        ELSE NULL
    END AS mom_growth_pct

FROM sales_with_previous
ORDER BY sales_month;
