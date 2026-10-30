from db_config import get_connection


def low_stock_report():
    query = """
        SELECT p.product_id, p.product_name, c.category_name,
               s.supplier_name, p.quantity_in_stock, p.reorder_level
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        JOIN suppliers  s ON p.supplier_id = s.supplier_id
        WHERE p.quantity_in_stock <= p.reorder_level
        ORDER BY p.quantity_in_stock ASC;
    """
    return _run(query)


def sales_by_category():
    query = """
        SELECT c.category_name,
               SUM(oi.quantity) AS units_sold,
               SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM order_items oi
        JOIN products p   ON oi.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        JOIN orders o     ON oi.order_id = o.order_id
        WHERE o.status = 'COMPLETED'
        GROUP BY c.category_name
        ORDER BY total_revenue DESC;
    """
    return _run(query)


def top_customers(limit=5):
    query = """
        SELECT cu.customer_id, cu.customer_name, cu.email,
               COUNT(DISTINCT o.order_id) AS total_orders,
               SUM(oi.quantity * oi.unit_price) AS total_spent
        FROM customers cu
        JOIN orders o      ON cu.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'COMPLETED'
        GROUP BY cu.customer_id, cu.customer_name, cu.email
        ORDER BY total_spent DESC
        LIMIT %s;
    """
    return _run(query, (limit,))


def monthly_revenue():
    query = """
        SELECT DATE_TRUNC('month', o.order_date) AS month,
               SUM(oi.quantity * oi.unit_price) AS total_revenue,
               COUNT(DISTINCT o.order_id) AS total_orders
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'COMPLETED'
        GROUP BY month
        ORDER BY month;
    """
    return _run(query)


def supplier_performance():
    query = """
        SELECT s.supplier_name,
               COUNT(DISTINCT p.product_id) AS products_supplied,
               COALESCE(SUM(oi.quantity), 0) AS units_sold,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
        FROM suppliers s
        JOIN products p ON s.supplier_id = p.supplier_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'COMPLETED'
        GROUP BY s.supplier_name
        ORDER BY total_revenue DESC;
    """
    return _run(query)


def _run(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()