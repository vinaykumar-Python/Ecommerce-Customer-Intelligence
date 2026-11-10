import sqlite3

DB_PATH = "database/ecommerce.db"

connection = sqlite3.connect(DB_PATH)

checks = {
    "Duplicate customer IDs": """
        SELECT COUNT(*) FROM (
            SELECT customer_id
            FROM customers
            GROUP BY customer_id
            HAVING COUNT(*) > 1
        )
    """,

    "Duplicate order IDs": """
        SELECT COUNT(*) FROM (
            SELECT order_id
            FROM orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        )
    """,

    "Duplicate product IDs": """
        SELECT COUNT(*) FROM (
            SELECT product_id
            FROM products
            GROUP BY product_id
            HAVING COUNT(*) > 1
        )
    """,

    "Duplicate seller IDs": """
        SELECT COUNT(*) FROM (
            SELECT seller_id
            FROM sellers
            GROUP BY seller_id
            HAVING COUNT(*) > 1
        )
    """,

    "Orders with unknown customers": """
        SELECT COUNT(*)
        FROM orders o
        LEFT JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """,

    "Order items with unknown orders": """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """,

    "Order items with unknown products": """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN products p
            ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL
    """,

    "Order items with unknown sellers": """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN sellers s
            ON oi.seller_id = s.seller_id
        WHERE s.seller_id IS NULL
    """,

    "Payments with unknown orders": """
        SELECT COUNT(*)
        FROM payments p
        LEFT JOIN orders o
            ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
    """,

    "Reviews with unknown orders": """
        SELECT COUNT(*)
        FROM reviews r
        LEFT JOIN orders o
            ON r.order_id = o.order_id
        WHERE o.order_id IS NULL
    """
}

print("\nDATA RELATIONSHIP VALIDATION")
print("=" * 65)

for check_name, query in checks.items():
    result = connection.execute(query).fetchone()[0]
    status = "PASS" if result == 0 else "CHECK"
    print(f"{check_name:<42} {result:>8}  {status}")

connection.close()
