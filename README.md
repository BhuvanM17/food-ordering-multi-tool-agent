# 🍔 ByteBite Bistro - AI Food Ordering Web Application

An autonomous, conversational food ordering web application powered by **FastAPI**, **Google Gemini 2.5**, and **SQLite**. The app features a modern web dashboard with an interactive menu, slide-out shopping cart, live order tracking, and a real-time AI Concierge powered by Gemini's tool-use function calling.

---

## ✨ Features

- 💬 **Live AI Concierge Chat**: Conversational food ordering powered by Google Gemini 2.5 (`gemini-2.5-flash-lite`) with multi-turn session memory and quick prompt chips.
- 🛠️ **Autonomous Tool Calling**: Gemini autonomously queries SQLite tables, updates shopping carts, places orders, and checks statuses.
- 🍕 **Interactive Visual Menu**: Category filters (*Burgers, Pizza, Sides, Drinks*), instant text search, price tags, and one-click "Add to Cart".
- 🛒 **Real-Time Shopping Cart Drawer**: Instant item counter, quantity increment/decrement controls, tax calculation (8%), and checkout buttons.
- 📦 **Order Tracking & Receipt Modal**: 4-stage visual progress stepper (*Confirmed* ➔ *Kitchen* ➔ *Out for Delivery* ➔ *Delivered*) and itemized receipts by Order ID.
- ⚡ **FastAPI Backend**: Asynchronous REST API serving both the single-page application and backend endpoints.

---

## 📂 Project Structure

```text
food_ordering_agent/
│
├── app.py              # FastAPI Web & REST API backend server
├── agent.py            # Gemini 2.5 Agent with session management & tool calling
├── database.py         # SQLite database schema, connection manager & menu seed
├── tools.py            # Python tool functions (search_menu, add_to_cart, etc.)
├── main.py             # Optional CLI chat interface
│
├── static/             # Frontend Web Assets
│   ├── css/
│   │   └── style.css   # Dark glassmorphic styling & micro-animations
│   ├── js/
│   │   └── app.js      # Client-side state, chat stream & cart synchronization
│   └── index.html      # Responsive single-page application UI
│
├── .env.example        # Environment variables template
├── .gitignore          # Ignores sensitive keys, SQLite DB, and caches
└── requirements.txt    # Project dependencies (FastAPI, Uvicorn, Gemini SDK)
```

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.10+** installed
- A **Gemini API Key** (Obtain one for free at [Google AI Studio](https://aistudio.google.com/app/apikey))

### 2. Clone the Repository

```bash
git clone https://github.com/BhuvanM17/food-ordering-multi-tool-agent.git
cd food-ordering-multi-tool-agent
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
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and set your key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 🎮 How to Run

### Option 1: Web Interface (Recommended)

Launch the FastAPI application:

```bash
python app.py
```
*(Or run with Uvicorn: `uvicorn app:app --reload --port 8000`)*

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

### Option 2: CLI Terminal Mode

You can also run the agent directly inside your terminal:

```bash
python main.py
```

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the single-page web app |
| `POST` | `/api/chat` | Sends message to Gemini AI Agent and returns response + cart state |
| `GET` | `/api/menu` | Fetches full restaurant menu and categories |
| `GET` | `/api/cart` | Gets active shopping cart state and totals |
| `POST` | `/api/cart/add` | Adds dish to cart |
| `POST` | `/api/cart/update` | Updates quantity of an item (+1 / -1) |
| `POST` | `/api/cart/clear` | Clears all items from cart |
| `POST` | `/api/orders/place` | Finalizes cart and creates order in SQLite |
| `GET` | `/api/orders/{id}` | Fetches tracking details and receipt for an order |

---

## 🛡️ Security

- The `.gitignore` prevents `.env` and local SQLite database files from being pushed to public version control.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
