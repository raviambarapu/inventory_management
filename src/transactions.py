from db_config import get_connection


def place_order(customer_id, items):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO orders (customer_id, status) VALUES (%s, 'PENDING') RETURNING order_id;",
                    (customer_id,),
                )
                order_id = cur.fetchone()["order_id"]

                for item in items:
                    product_id = item["product_id"]
                    qty = item["quantity"]

                    cur.execute(
                        "SELECT unit_price, quantity_in_stock FROM products "
                        "WHERE product_id = %s FOR UPDATE;",
                        (product_id,),
                    )
                    product = cur.fetchone()
                    if product is None:
                        raise ValueError(f"Product {product_id} does not exist.")
                    if product["quantity_in_stock"] < qty:
                        raise ValueError(
                            f"Insufficient stock for product {product_id}: "
                            f"requested {qty}, available {product['quantity_in_stock']}."
                        )

                    cur.execute(
                        """INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                           VALUES (%s, %s, %s, %s);""",
                        (order_id, product_id, qty, product["unit_price"]),
                    )

                    cur.execute(
                        "UPDATE products SET quantity_in_stock = quantity_in_stock - %s "
                        "WHERE product_id = %s;",
                        (qty, product_id),
                    )

                cur.execute(
                    "UPDATE orders SET status = 'COMPLETED' WHERE order_id = %s;",
                    (order_id,),
                )

        return order_id
    finally:
        conn.close()


def cancel_order(order_id):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT product_id, quantity FROM order_items WHERE order_id = %s;",
                    (order_id,),
                )
                items = cur.fetchall()
                if not items:
                    raise ValueError(f"Order {order_id} not found or has no items.")

                for item in items:
                    cur.execute(
                        "UPDATE products SET quantity_in_stock = quantity_in_stock + %s "
                        "WHERE product_id = %s;",
                        (item["quantity"], item["product_id"]),
                    )

                cur.execute(
                    "UPDATE orders SET status = 'CANCELLED' WHERE order_id = %s;",
                    (order_id,),
                )
        return True
    finally:
        conn.close()