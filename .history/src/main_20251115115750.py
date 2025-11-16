#!/usr/bin/env python3
"""
Main entry point for the AI Psychologist application
"""

import argparse
import sys
import traceback

from ai_psychologist import AIPsychologist

def main():
    parser = argparse.ArgumentParser(description="AI Psychologist with Long-Term Memory")
    parser.add_argument("--user-id", required=True, help="User ID for memory isolation")
    
    args = parser.parse_args()
    
    # Create an instance of the AI Psychologist
    psychologist = AIPsychologist(args.user_id)
    
    print("Welcome to the AI Psychologist. Type 'quit' to exit.")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '再见', '退出']:
                print("\nAI Psychologist: Take care! Feel free to come back anytime you need support.")
                break
            
            if user_input:
                response = psychologist.chat(user_input)
                print(f"\nAI Psychologist: {response}")
                
        except KeyboardInterrupt:
            print("\n\nAI Psychologist: Take care! Feel free to come back anytime you need support.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again or restart the application.")
            # 打印完整的错误堆栈以便调试
            traceback.print_exc()

if __name__ == "__main__":
    main()