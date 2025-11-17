#!/usr/bin/env python3
"""
Test script for AI Virtual Assistant for Students
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from src.assistant_pipeline import AssistantPipeline
        print("✅ AssistantPipeline imported successfully")
    except Exception as e:
        print(f"❌ Failed to import AssistantPipeline: {e}")
        return False
    
    try:
        from src.components.nlp_core import NLPCore
        print("✅ NLPCore imported successfully")
    except Exception as e:
        print(f"❌ Failed to import NLPCore: {e}")
        return False
    
    try:
        from src.components.knowledge_graph import KnowledgeGraph
        print("✅ KnowledgeGraph imported successfully")
    except Exception as e:
        print(f"❌ Failed to import KnowledgeGraph: {e}")
        return False
    
    try:
        from src.components.speech_to_text import SpeechToText
        print("✅ SpeechToText imported successfully")
    except Exception as e:
        print(f"❌ Failed to import SpeechToText: {e}")
        return False
    
    try:
        from src.components.text_to_speech import TextToSpeech
        print("✅ TextToSpeech imported successfully")
    except Exception as e:
        print(f"❌ Failed to import TextToSpeech: {e}")
        return False
    
    return True

def test_knowledge_graph():
    """Test knowledge graph functionality."""
    print("\n📚 Testing Knowledge Graph...")
    
    try:
        from src.components.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()
        
        # Test entity extraction
        entities = kg.extract_entities("What is photosynthesis?")
        print(f"✅ Entity extraction: {entities}")
        
        # Test knowledge query
        context = kg.query_knowledge_base(entities)
        if context:
            print(f"✅ Knowledge query successful: {context[:100]}...")
        else:
            print("⚠️  No knowledge context found (this is normal for some queries)")
        
        return True
    except Exception as e:
        print(f"❌ Knowledge graph test failed: {e}")
        return False

def test_nlp_core():
    """Test NLP core functionality."""
    print("\n🧠 Testing NLP Core...")
    
    try:
        from src.components.nlp_core import NLPCore
        nlp = NLPCore()
        
        # Test response generation (will work even without API key)
        response = nlp.generate_response("Hello, how are you?")
        print(f"✅ NLP response: {response[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ NLP core test failed: {e}")
        return False

def test_assistant_pipeline():
    """Test the main assistant pipeline."""
    print("\n🎯 Testing Assistant Pipeline...")
    
    try:
        from src.assistant_pipeline import AssistantPipeline
        assistant = AssistantPipeline()
        
        # Test text message processing
        response = assistant.process_text_message("What is artificial intelligence?")
        print(f"✅ Pipeline response: {response[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ Assistant pipeline test failed: {e}")
        return False

def main():
    print("🎓 AI Virtual Assistant - Component Tests")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return False
    
    # Test knowledge graph
    if not test_knowledge_graph():
        print("\n❌ Knowledge graph tests failed.")
        return False
    
    # Test NLP core
    if not test_nlp_core():
        print("\n❌ NLP core tests failed.")
        return False
    
    # Test assistant pipeline
    if not test_assistant_pipeline():
        print("\n❌ Assistant pipeline tests failed.")
        return False
    
    print("\n🎉 All tests passed! Your AI Virtual Assistant is ready to use.")
    print("\nTo start the web interface, run: python app.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
