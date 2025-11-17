#!/usr/bin/env python3
"""
Test script to verify AI response improvements
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_ai_response():
    """Test the AI response generation."""
    try:
        from simple_app import generate_simple_response
        
        # Test questions
        test_questions = [
            "What is photosynthesis?",
            "How does AI work?",
            "Tell me about Einstein",
            "What are neural networks?"
        ]
        
        print("🧪 Testing AI Response Improvements")
        print("=" * 50)
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            response = generate_simple_response(question)
            print(f"Response: {response}")
            print(f"Length: {len(response)} characters")
            print("-" * 40)
            
    except Exception as e:
        print(f"Error testing responses: {e}")

if __name__ == "__main__":
    test_ai_response()
