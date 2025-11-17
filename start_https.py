#!/usr/bin/env python3
"""
Start the AI Virtual Assistant with HTTPS enabled
"""

import os
import subprocess
import sys

def main():
    print("🔒 Starting AI Virtual Assistant with HTTPS...")
    print("This will enable microphone access from external domains.")
    print()
    
    # Set the environment variable for HTTPS
    os.environ['USE_HTTPS'] = 'true'
    
    try:
        # Import and run the main app
        from app import app
        
        print("🚀 Starting AI Virtual Assistant...")
        print("🔒 HTTPS is enabled!")
        print("The application will be available at: https://localhost:5000")
        print()
        print("⚠️  Note: You may see a security warning - this is normal for self-signed certificates.")
        print("   Click 'Advanced' and 'Proceed to localhost' to continue.")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Create SSL context and run
        from app import create_ssl_context
        
        cert_path, key_path = create_ssl_context()
        if cert_path and key_path:
            app.run(debug=False, host='0.0.0.0', port=5000, ssl_context=(cert_path, key_path))
        else:
            print("❌ Failed to create SSL certificate. Please install cryptography:")
            print("   pip install cryptography")
            sys.exit(1)
            
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        print("Make sure you're in the correct directory and all dependencies are installed.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
