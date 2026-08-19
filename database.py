import sqlite3
from contextlib import contextmanager

DB_NAME = "food_ordering.db"

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Menu table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                price REAL NOT NULL,
                description TEXT
            )
        """)
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                items TEXT NOT NULL,          -- JSON string of items
                total REAL NOT NULL,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Seed some menu items (only if empty)
        cursor.execute("SELECT COUNT(*) FROM menu")
        if cursor.fetchone()[0] == 0:
            sample_menu = [
                ("Chicken Burger", "Burgers", 8.99, "Juicy chicken patty with lettuce & mayo"),
                ("Veggie Burger", "Burgers", 7.49, "Fresh vegetable patty with special sauce"),
                ("Cheese Burger", "Burgers", 9.49, "Classic beef with melted cheese"),
                ("Coke", "Drinks", 1.99, "Chilled Coca-Cola 330ml"),
                ("Pepsi", "Drinks", 1.99, "Chilled Pepsi 330ml"),
                ("French Fries", "Sides", 3.49, "Crispy golden fries"),
                ("Chicken Wings", "Sides", 6.99, "Spicy chicken wings (6 pcs)"),
                ("Margherita Pizza", "Pizza", 11.99, "Classic cheese & tomato pizza"),
            ]
            cursor.executemany(
                "INSERT INTO menu (name, category, price, description) VALUES (?, ?, ?, ?)",
                sample_menu
            )
        
        conn.commit()

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()