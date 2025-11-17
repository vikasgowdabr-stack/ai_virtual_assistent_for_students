#!/usr/bin/env python3
"""
Test script for Google API Key setup
"""

import os
import sys

def test_api_key():
    """Test if the Google API key is set up correctly."""
    print("🔑 Testing Google API Key Setup")
    print("=" * 40)
    
    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Check if API key is set
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ API Key not found!")
        print("\nTo set up your API key:")
        print("1. Get your key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as environment variable:")
        print("   export GOOGLE_API_KEY='your_key_here'")
        print("3. Or create a .env file with: GOOGLE_API_KEY=your_key_here")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test the API key
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Test with a simple request
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content('Hello, how are you?')
        
        print("✅ API Key is working!")
        print(f"Test response: {response.text[:100]}...")
        return True
        
    except ImportError:
        print("❌ google-generativeai not installed!")
        print("Install it with: pip install google-generativeai")
        return False
        
    except Exception as e:
        print(f"❌ API Key test failed: {e}")
        print("Please check your API key and try again.")
        return False

def test_voice_dependencies():
    """Test if voice dependencies are installed."""
    print("\n🎤 Testing Voice Dependencies")
    print("=" * 40)
    
    voice_ok = True
    
    try:
        import pyaudio
        print("✅ PyAudio installed")
    except ImportError:
        print("❌ PyAudio not installed")
        print("Install with: pip install pyaudio")
        voice_ok = False
    
    try:
        import webrtcvad
        print("✅ WebRTC VAD installed")
    except ImportError:
        print("❌ WebRTC VAD not installed")
        print("Install with: pip install webrtcvad")
        voice_ok = False
    
    return voice_ok

def main():
    """Main test function."""
    print("🎓 AI Virtual Assistant - Setup Test")
    print("=" * 50)
    
    # Test API key
    api_ok = test_api_key()
    
    # Test voice dependencies
    voice_ok = test_voice_dependencies()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    print(f"API Key: {'✅ Working' if api_ok else '❌ Not set up'}")
    print(f"Voice Dependencies: {'✅ Ready' if voice_ok else '❌ Missing'}")
    
    if api_ok and voice_ok:
        print("\n🎉 Everything is ready!")
        print("You can run the full application with:")
        print("python app.py")
    elif api_ok:
        print("\n⚠️  API key is working, but voice features need setup.")
        print("Install voice dependencies: pip install pyaudio webrtcvad")
    else:
        print("\n⚠️  Please set up your API key first.")
        print("See API_SETUP.md for detailed instructions.")
    
    print("\nFor now, you can use the simple app:")
    print("python simple_app.py")

if __name__ == "__main__":
    main()
