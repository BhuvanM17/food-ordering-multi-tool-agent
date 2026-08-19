import json
from database import get_connection

cart = []

def search_menu(query: str) -> str:
    """Search the menu for food items by name, category, or description."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, category, price, description 
            FROM menu 
            WHERE name LIKE ? OR category LIKE ? OR description LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))

        rows = cursor.fetchall()
        if not rows:
            return f"No items found for '{query}'."
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "price": row["price"],
                "description": row["description"]
            })
        return json.dumps(result, indent=2)


def add_to_cart(item_id: int, quantity: int = 1) -> str:
    """Add a menu item to the cart using its ID and quantity."""
    global cart
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM menu WHERE id = ?", (item_id,))
        row = cursor.fetchone()

        if not row:
            return f"Item {item_id} not found."
        
        for item in cart:
            if item["id"] == item_id:
                item["quantity"] += quantity
                return f"Updated quantity of {row['name']} to {item['quantity']}."
        
        cart.append({
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "quantity": quantity
        })
        return f"Added {quantity} of {row['name']} to cart."


def view_cart() -> str:
    """View the current cart contents and total price."""
    if not cart:
        return "Your cart is empty."
    
    total = 0
    lines = ["Current Cart:"]
    for item in cart:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        lines.append(f"- {item['quantity']} x {item['name']} (${item['price']:.2f}) = ${subtotal:.2f}")
    
    lines.append(f"\nTotal: ${total:.2f}")
    return "\n".join(lines)


def place_order() -> str:
    """Place the current cart as a confirmed order."""
    global cart
    if not cart:
        return "Cart is empty, cannot place order."
    
    total = sum(item["price"] * item["quantity"] for item in cart)
    items_json = json.dumps(cart)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (items, total, status) VALUES (?, ?, ?)",
            (items_json, total, "Confirmed")
        )
        order_id = cursor.lastrowid
        conn.commit()
    
    cart = []  # clear cart
    return f"Order placed successfully! Order ID: {order_id}, Total: ${total:.2f}, Status: Confirmed"


def track_order(order_id: int) -> str:
    """Track an existing order using its order ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, total, status, created_at FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()

        if not row:
            return f"Order ID {order_id} not found."

        return (f"Order ID: {row['id']}\n"
                f"Total: ${row['total']:.2f}\n"
                f"Status: {row['status']}\n"
                f"Placed at: {row['created_at']}")


# ==================== API Helper Functions ====================

def get_cart_data():
    """Return raw cart data and calculated totals for the frontend."""
    subtotal = sum(item["price"] * item["quantity"] for item in cart)
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + tax, 2)
    return {
        "items": list(cart),
        "subtotal": round(subtotal, 2),
        "tax": tax,
        "total": total,
        "count": sum(item["quantity"] for item in cart)
    }


def update_cart_item_quantity(item_id: int, delta: int):
    """Adjust quantity of an item in the cart, removing it if quantity reaches 0."""
    global cart
    for item in cart:
        if item["id"] == item_id:
            item["quantity"] += delta
            if item["quantity"] <= 0:
                cart.remove(item)
            break
    return get_cart_data()


def remove_cart_item(item_id: int):
    """Remove an item completely from cart."""
    global cart
    cart = [item for item in cart if item["id"] != item_id]
    return get_cart_data()


def clear_cart_data():
    """Clear all items from cart."""
    global cart
    cart = []
    return get_cart_data()


def get_all_menu():
    """Fetch all menu items from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, price, description FROM menu ORDER BY category, name")
        rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "price": row["price"],
                "description": row["description"]
            }
            for row in rows
        ]


def get_order_details(order_id: int):
    """Fetch structured order details by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, items, total, status, created_at FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "items": json.loads(row["items"]),
            "total": row["total"],
            "status": row["status"],
            "created_at": row["created_at"]
        }