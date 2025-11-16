#!/usr/bin/env python3
"""
Demonstration script for the AI Psychologist
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def run_demo():
    """Run a demonstration of the AI Psychologist capabilities"""
    try:
        from ai_psychologist import AIPsychologist
        
        print("AI Psychologist Demonstration")
        print("=" * 40)
        print("This demo will show the capabilities of the AI Psychologist")
        print("with long-term memory.\n")
        
        # Create psychologist instance
        psychologist = AIPsychologist("demo_user")
        
        # Reset memory for clean demo
        psychologist.reset_memory()
        print("✓ Memory reset for demo")
        
        # Demo conversation
        demo_conversations = [
            ("Hello, I've been feeling quite anxious lately.", "Initial anxiety expression"),
            ("It's mainly about my upcoming job interview next week.", "Specific anxiety trigger"),
            ("I'm worried I won't perform well and will disappoint my family.", "Underlying concerns"),
            ("That makes sense. Can you tell me more about your previous interview experiences?", "Follow-up question"),
            ("Actually, I'm also feeling a bit sad about a recent breakup.", "Additional emotional context"),
            ("How has that breakup affected your daily life?", "Exploring impact"),
        ]
        
        print("\nDemo Conversation:")
        print("-" * 20)
        
        for i, (message, description) in enumerate(demo_conversations, 1):
            print(f"\n[{i}] {description}")
            print(f"User: {message}")
            
            response = psychologist.chat(message)
            print(f"AI Psychologist: {response}")
            
            # Show memory state after a few interactions
            if i == 3:
                print("\n[Memory System Status]")
                user_profile = psychologist.memory_system.get_user_profile()
                if user_profile.get("personality_insights"):
                    print(f"Personality Insights: {user_profile['personality_insights']}")
                print(f"Episodic Memories: {len(psychologist.memory_system.episodic_memory)} conversations stored")
        
        print("\n" + "=" * 40)
        print("Demo completed successfully!")
        print("\nKey Features Demonstrated:")
        print("1. Multi-turn conversation with context retention")
        print("2. Emotion detection and appropriate responses")
        print("3. Memory building across conversations")
        print("4. Personality insights tracking")
        print("5. Long-term memory storage")
        
        # Reset memory after demo
        psychologist.reset_memory()
        print("\n✓ Memory reset after demo")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    print("AI Psychologist Demo Script")
    print("=" * 30)
    
    if run_demo():
        print("\n✅ Demo completed successfully!")
        print("\nTo run the full interactive application:")
        print("  python src/main.py")
    else:
        print("\n❌ Demo failed. Please check the error above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())