import os
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database import init_db
from agent import run_agent
from tools import (
    get_all_menu,
    get_cart_data,
    add_to_cart,
    update_cart_item_quantity,
    remove_cart_item,
    clear_cart_data,
    place_order,
    get_order_details,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and seed menu
    init_db()
    yield

app = FastAPI(
    title="ByteBite AI Food Ordering API",
    description="FastAPI backend for Food Ordering Multi-Tool Agent",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static assets with robust absolute paths
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

css_dir = os.path.join(STATIC_DIR, "css")
js_dir = os.path.join(STATIC_DIR, "js")
if os.path.exists(css_dir):
    app.mount("/css", StaticFiles(directory=css_dir), name="css")
if os.path.exists(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")


# ==================== Request / Response Models ====================

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class CartAddRequest(BaseModel):
    item_id: int
    quantity: int = 1

class CartUpdateRequest(BaseModel):
    item_id: int
    delta: int

class CartRemoveRequest(BaseModel):
    item_id: int


# ==================== Routes ====================

@app.get("/")
async def root():
    """Serve the single-page web app."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_path)


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """Handle conversational chat requests with the Gemini Agent."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    reply, session_id = run_agent(req.message, session_id=req.session_id)
    cart_state = get_cart_data()
    return {
        "reply": str(reply) if reply else "",
        "session_id": str(session_id),
        "cart": cart_state
    }


@app.get("/api/menu")
async def menu_endpoint():
    """Retrieve full menu items and category list."""
    items = get_all_menu()
    categories = sorted(list(set(item["category"] for item in items)))
    return {
        "items": items,
        "categories": categories
    }


@app.get("/api/cart")
async def cart_endpoint():
    """Retrieve current shopping cart state."""
    return get_cart_data()


@app.post("/api/cart/add")
async def add_cart_endpoint(req: CartAddRequest):
    """Add item to cart directly via UI."""
    msg = add_to_cart(req.item_id, req.quantity)
    return {
        "message": msg,
        "cart": get_cart_data()
    }


@app.post("/api/cart/update")
async def update_cart_endpoint(req: CartUpdateRequest):
    """Update item quantity (+1 or -1)."""
    return update_cart_item_quantity(req.item_id, req.delta)


@app.post("/api/cart/remove")
async def remove_cart_endpoint(req: CartRemoveRequest):
    """Remove item from cart."""
    return remove_cart_item(req.item_id)


@app.post("/api/cart/clear")
async def clear_cart_endpoint():
    """Clear all items in cart."""
    return clear_cart_data()


@app.post("/api/orders/place")
async def place_order_endpoint():
    """Directly place order from cart."""
    msg = place_order()
    return {
        "message": msg,
        "cart": get_cart_data()
    }


@app.get("/api/orders/{order_id}")
async def get_order_endpoint(order_id: int):
    """Retrieve order details and status for tracking."""
    order = get_order_details(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order #{order_id} not found.")
    return {"order": order}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
