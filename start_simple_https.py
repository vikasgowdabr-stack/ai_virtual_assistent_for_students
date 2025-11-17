#!/usr/bin/env python3
"""
Start the Simple AI Virtual Assistant with HTTPS enabled
"""

import os
import sys

def main():
    print("🔒 Starting Simple AI Virtual Assistant with HTTPS...")
    print("This will enable microphone access from external domains.")
    print()
    
    # Set the environment variable for HTTPS
    os.environ['USE_HTTPS'] = 'true'
    
    try:
        # Import and run the simple app
        from simple_app import main as simple_main
        
        print("🚀 Starting Simple AI Virtual Assistant...")
        print("🔒 HTTPS is enabled!")
        print("The application will be available at: https://localhost:8080")
        print()
        print("⚠️  Note: You may see a security warning - this is normal for self-signed certificates.")
        print("   Click 'Advanced' and 'Proceed to localhost' to continue.")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the simple app
        simple_main()
            
    except ImportError as e:
        print(f"❌ Error importing simple_app: {e}")
        print("Make sure you're in the correct directory and all dependencies are installed.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
