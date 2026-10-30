import sys
sys.path.append("src")

import crud_operations as crud
import transactions as txn
import reports


def print_rows(rows):
    if not rows:
        print("  (no rows)")
        return
    for row in rows:
        print(" ", dict(row))


def menu():
    print("""
==== INVENTORY MANAGEMENT SYSTEM ====
1. List all products
2. Add a product
3. Update product stock/price
4. Delete a product
5. Place an order (transaction demo)
6. Cancel an order
7. Low stock report
8. Sales by category report
9. Top customers report
10. Monthly revenue report
11. Supplier performance report
0. Exit
""")


def main():
    while True:
        menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                print_rows(crud.get_all_products())

            elif choice == "2":
                name = input("Product name: ")
                category_id = int(input("Category ID: "))
                supplier_id = int(input("Supplier ID: "))
                price = float(input("Unit price: "))
                qty = int(input("Quantity in stock: "))
                new_id = crud.add_product(name, category_id, supplier_id, price, qty)
                print(f"Created product with ID {new_id}")

            elif choice == "3":
                pid = int(input("Product ID: "))
                price = input("New unit price (blank to skip): ")
                qty = input("New quantity (blank to skip): ")
                fields = {}
                if price:
                    fields["unit_price"] = float(price)
                if qty:
                    fields["quantity_in_stock"] = int(qty)
                ok = crud.update_product(pid, **fields)
                print("Updated." if ok else "No such product.")

            elif choice == "4":
                pid = int(input("Product ID to delete: "))
                ok = crud.delete_product(pid)
                print("Deleted." if ok else "No such product.")

            elif choice == "5":
                cid = int(input("Customer ID: "))
                items = []
                while True:
                    pid = input("Product ID (blank to finish order): ")
                    if not pid:
                        break
                    qty = int(input("  Quantity: "))
                    items.append({"product_id": int(pid), "quantity": qty})
                order_id = txn.place_order(cid, items)
                print(f"Order placed successfully. Order ID: {order_id}")

            elif choice == "6":
                oid = int(input("Order ID to cancel: "))
                txn.cancel_order(oid)
                print("Order cancelled and stock restored.")

            elif choice == "7":
                print_rows(reports.low_stock_report())

            elif choice == "8":
                print_rows(reports.sales_by_category())

            elif choice == "9":
                print_rows(reports.top_customers())

            elif choice == "10":
                print_rows(reports.monthly_revenue())

            elif choice == "11":
                print_rows(reports.supplier_performance())

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid option, try again.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()