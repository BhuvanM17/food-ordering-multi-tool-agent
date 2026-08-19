# 🍔 AI Food Ordering Agent

An autonomous, conversational food ordering agent powered by **Google Gemini 2.5** and **Python**. The agent interacts with users in natural language, searches restaurant menus, manages shopping carts, places orders, and tracks existing orders using Gemini function calling (Tool Use) and an SQLite backend.

---

## ✨ Features

- 💬 **Natural Language Ordering**: Understands conversational multi-item requests (e.g. *"Can I get 2 chicken burgers and a chilled coke?"*).
- 🛠️ **Automatic Tool Calling**: Powered by Gemini 2.5 function calling to autonomously query databases and trigger actions.
- 📋 **Menu Search**: Dynamically searches dishes by name, category, or description.
- 🛒 **Cart Management**: Real-time item additions, quantity updates, and cart calculations.
- 📦 **Order Placement & Tracking**: Generates unique order IDs and stores order details in SQLite.
- 🔄 **Multi-Turn Memory**: Preserves context across the entire conversation.

---

## 📂 Project Structure

```text
food_ordering_agent/
│
├── agent.py            # AI Agent configuration & Gemini tool execution loop
├── database.py         # SQLite database initialization & sample menu seeding
├── tools.py            # Real Python tool functions (search, cart, order, track)
├── main.py             # CLI chat interface and interaction loop
│
├── .env.example        # Environment variable template
├── .gitignore          # Ignores sensitive keys, SQLite DB, and caches
└── requirements.txt    # Project dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.10+** installed
- A **Gemini API Key** (Obtain one for free at [Google AI Studio](https://aistudio.google.com/app/apikey))

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/food_ordering_agent.git
cd food_ordering_agent
```

### 3. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS / Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

Create a `.env` file from `.env.example`:

```bash
# Windows PowerShell
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and paste your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 🎮 How to Run

Launch the CLI agent:

```bash
python main.py
```

### Example Interaction

```text
🍔 Food Ordering AI Agent (Pure Python Version)
Type 'quit' to exit

You: Hi, what burgers do you have?
Agent: We have the following burgers on our menu:
- Chicken Burger: Juicy chicken patty with lettuce & mayo ($8.99)
- Veggie Burger: Fresh vegetable patty with special sauce ($7.49)
- Cheese Burger: Classic beef with melted cheese ($9.49)

You: Add 2 chicken burgers and 1 coke to my cart
Agent: Added 2 Chicken Burger and 1 Coke to your cart. 

Current Cart:
- 2 x Chicken Burger ($8.99) = $17.98
- 1 x Coke ($1.99) = $1.99
Total: $19.97

You: Place my order
Agent: Order placed successfully! Order ID: 1, Total: $19.97, Status: Confirmed.

You: Track order 1
Agent: Order ID: 1
Total: $19.97
Status: Confirmed
Placed at: 2026-08-19 08:15:30
```

---

## 🛠️ Available Tools

| Tool Function | Description |
| :--- | :--- |
| `search_menu(query)` | Searches menu items by keyword, category, or description |
| `add_to_cart(item_id, quantity)` | Adds items to the active cart or updates quantities |
| `view_cart()` | Displays all items in the cart and subtotal/total |
| `place_order()` | Finalizes the cart and records the order into SQLite |
| `track_order(order_id)` | Looks up order status and timestamps |

---

## 🛡️ Security Notes

- **Never commit your `.env` file** to GitHub. The included `.gitignore` prevents `.env` and local `.db` files from being tracked.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
