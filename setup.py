#!/usr/bin/env python3
"""
Setup script for AI Virtual Assistant for Students
"""

import os
import sys
import subprocess
import json

def print_banner():
    print("🎓" * 50)
    print("🎓 AI Virtual Assistant for Students - Setup")
    print("🎓" * 50)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        return False

def setup_api_key():
    """Help user set up Google API key."""
    print("\n🔑 Google API Key Setup")
    print("To use Gemini features, you need a Google API key.")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Copy the key")
    
    api_key = input("\nEnter your Google API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Create .env file
        with open('.env', 'w') as f:
            f.write(f'GOOGLE_API_KEY={api_key}\n')
        print("✅ API key saved to .env file")
        return True
    else:
        print("⚠️  No API key provided. Gemini features will be disabled.")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ['data', 'templates', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created")

def test_installation():
    """Test if the installation works."""
    print("\n🧪 Testing installation...")
    try:
        # Test imports
        import flask
        import transformers
        import google.generativeai
        print("✅ All core libraries imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_application():
    """Run the application."""
    print("\n🚀 Starting AI Virtual Assistant...")
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

def main():
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup API key
    setup_api_key()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    
    # Ask if user wants to run the application
    run_now = input("\nWould you like to start the application now? (y/n): ").lower().strip()
    if run_now in ['y', 'yes']:
        run_application()

if __name__ == "__main__":
    main()
