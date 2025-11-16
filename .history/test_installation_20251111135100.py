#!/usr/bin/env python3
"""
Test script to verify AI Psychologist installation
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    # Add src to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from ai_psychologist import AIPsychologist
        print("✓ AI Psychologist module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import AI Psychologist module: {e}")
        return False
    
    try:
        from config import Config
        print("✓ Config module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Config module: {e}")
        return False
    
    # Test conditional imports
    try:
        import openai
        print("✓ OpenAI library available")
    except ImportError:
        print("! OpenAI library not installed (using mock responses)")
    
    try:
        import chromadb
        print("✓ ChromaDB library available")
    except ImportError:
        print("! ChromaDB library not installed (using file-based storage)")
    
    return True

def test_basic_functionality():
    """Test basic functionality without API key"""
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from ai_psychologist import AIPsychologist
        
        # Create psychologist instance
        psychologist = AIPsychologist("test_user")
        print("✓ AI Psychologist instance created successfully")
        
        # Test mock response
        response = psychologist.chat("I'm feeling sad today.")
        print(f"✓ Mock response generated: {response[:50]}...")
        
        # Test memory functionality
        psychologist.reset_memory()
        print("✓ Memory reset functionality works")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    print("AI Psychologist Installation Test")
    print("=" * 40)
    
    print("\n1. Testing imports...")
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return 1
    
    print("\n2. Testing basic functionality...")
    if not test_basic_functionality():
        print("\n❌ Functionality tests failed.")
        return 1
    
    print("\n✅ All tests passed! Installation appears to be working correctly.")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and add your OpenRouter API key")
    print("2. Run 'python src/main.py' to start the application")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())