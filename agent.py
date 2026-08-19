import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import search_menu, add_to_cart, view_cart, place_order, track_order

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """You are a helpful Food Ordering AI Agent for a restaurant.
You can search the menu, add items to cart, view cart, place orders and track orders.
Always be friendly and concise.
When the user wants multiple items, search first, then add them one by one.
After adding items, you can show the cart if helpful.
"""

def run_agent(user_message: str, conversation_history=None):
    """Runs the agent using Gemini's native chat session with automatic tool execution."""
    # Initialize a new chat session if none exists or if an empty list was passed from main.py
    if conversation_history is None or not hasattr(conversation_history, "send_message"):
        conversation_history = client.chats.create(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[search_menu, add_to_cart, view_cart, place_order, track_order],
                temperature=0.0,
            )
        )
    
    chat_session = conversation_history
    response = chat_session.send_message(user_message)
    return response.text, chat_session