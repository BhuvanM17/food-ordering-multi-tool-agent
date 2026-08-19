from database import init_db
from agent import run_agent

def main():
    print("🍔 Food Ordering AI Agent (Pure Python Version)")
    print("Type 'quit' to exit\n")
    
    init_db()  # create tables + seed menu
    
    history = []
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        answer, history = run_agent(user_input, history)
        print(f"\nAgent: {answer}\n")

if __name__ == "__main__":
    main()