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