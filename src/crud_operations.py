from db_config import get_connection


def add_product(name, category_id, supplier_id, unit_price, quantity, reorder_level=10):
    query = """
        INSERT INTO products (product_name, category_id, supplier_id,
                               unit_price, quantity_in_stock, reorder_level)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING product_id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, category_id, supplier_id, unit_price, quantity, reorder_level))
            new_id = cur.fetchone()["product_id"]
            conn.commit()
            return new_id


def get_all_products():
    query = "SELECT * FROM products ORDER BY product_id;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


def get_product_by_id(product_id):
    query = "SELECT * FROM products WHERE product_id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (product_id,))
            return cur.fetchone()


def update_product(product_id, **fields):
    if not fields:
        return False
    columns = ", ".join(f"{key} = %s" for key in fields)
    values = list(fields.values()) + [product_id]
    query = f"UPDATE products SET {columns} WHERE product_id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
            return cur.rowcount > 0


def delete_product(product_id):
    query = "DELETE FROM products WHERE product_id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (product_id,))
            conn.commit()
            return cur.rowcount > 0


def add_customer(name, email, phone=None, address=None):
    query = """
        INSERT INTO customers (customer_name, email, phone, address)
        VALUES (%s, %s, %s, %s) RETURNING customer_id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, email, phone, address))
            new_id = cur.fetchone()["customer_id"]
            conn.commit()
            return new_id


def get_all_customers():
    query = "SELECT * FROM customers ORDER BY customer_id;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


def update_customer(customer_id, **fields):
    if not fields:
        return False
    columns = ", ".join(f"{key} = %s" for key in fields)
    values = list(fields.values()) + [customer_id]
    query = f"UPDATE customers SET {columns} WHERE customer_id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
            return cur.rowcount > 0


def delete_customer(customer_id):
    query = "DELETE FROM customers WHERE customer_id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (customer_id,))
            conn.commit()
            return cur.rowcount > 0


def add_category(name, description=None):
    query = "INSERT INTO categories (category_name, description) VALUES (%s, %s) RETURNING category_id;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, description))
            new_id = cur.fetchone()["category_id"]
            conn.commit()
            return new_id


def add_supplier(name, email=None, phone=None, address=None):
    query = """
        INSERT INTO suppliers (supplier_name, contact_email, phone, address)
        VALUES (%s, %s, %s, %s) RETURNING supplier_id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, email, phone, address))
            new_id = cur.fetchone()["supplier_id"]
            conn.commit()
            return new_id