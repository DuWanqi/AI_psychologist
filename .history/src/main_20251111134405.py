#!/usr/bin/env python3
"""
Main entry point for the AI Psychologist application
"""

import argparse
import sys
import os

# Add the src directory to the path so we can import ai_psychologist
sys.path.append(os.path.join(os.path.dirname(__file__)))

from ai_psychologist import AIPsychologist


def main():
    parser = argparse.ArgumentParser(description="AI Psychologist - An empathetic mental health chatbot with long-term memory")
    parser.add_argument("--user-id", default="default_user", help="User ID for session management")
    parser.add_argument("--reset-memory", action="store_true", help="Reset all memory for the user")
    
    args = parser.parse_args()
    
    # Initialize the AI Psychologist
    psychologist = AIPsychologist(user_id=args.user_id)
    
    # Reset memory if requested
    if args.reset_memory:
        psychologist.reset_memory()
        print("Memory has been reset for user:", args.user_id)
    
    # Start the conversation loop
    print("Welcome to the AI Psychologist. Type 'quit' to exit.")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("AI Psychologist: Take care! Feel free to come back anytime you need support.")
                break
            
            if user_input:
                response = psychologist.chat(user_input)
                print(f"AI Psychologist: {response}")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again or restart the application.")


if __name__ == "__main__":
    main()