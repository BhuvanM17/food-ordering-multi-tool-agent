import os
import uuid
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import search_menu, add_to_cart, view_cart, place_order, track_order

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """You are a helpful Food Ordering AI Agent for a restaurant called 'ByteBite Bistro'.
You can search the menu, add items to cart, view cart, place orders and track orders.
Always be friendly, appetizing, and concise.
When the user wants multiple items, search first if needed, then add them one by one.
After adding items or placing orders, provide a clear, formatted summary.
"""

_sessions = {}

def get_or_create_chat_session(session_id: str = None):
    if not session_id or not isinstance(session_id, str):
        session_id = str(uuid.uuid4())
    
    if session_id not in _sessions:
        _sessions[session_id] = client.chats.create(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[search_menu, add_to_cart, view_cart, place_order, track_order],
                temperature=0.2,
            )
        )
    return session_id, _sessions[session_id]

def run_agent(user_message: str, conversation_history=None, session_id: str = None):
    """Runs the agent using Gemini's native chat session with automatic tool execution."""
    # Web API mode: always return (str_reply, str_session_id)
    if session_id is not None or conversation_history is None:
        sid, chat_session = get_or_create_chat_session(session_id)
        response = chat_session.send_message(user_message)
        return response.text or "", sid

    # Fallback for CLI main.py
    if not hasattr(conversation_history, "send_message"):
        conversation_history = client.chats.create(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[search_menu, add_to_cart, view_cart, place_order, track_order],
                temperature=0.2,
            )
        )
    
    chat_session = conversation_history
    response = chat_session.send_message(user_message)
    return response.text or "", chat_session