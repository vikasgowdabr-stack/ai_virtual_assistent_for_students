#!/usr/bin/env python3
"""
Startup script for AI Virtual Assistant for Students
"""

import os
import sys
import traceback

def main():
    print("🎓 AI Virtual Assistant for Students")
    print("=" * 50)
    
    try:
        # Import and run the main application
        from app import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\nFull error details:")
        traceback.print_exc()
        
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if you have enough disk space for model downloads")
        print("3. If you have a GPU, try setting CUDA_VISIBLE_DEVICES='' to use CPU only")
        print("4. Check the logs above for specific error messages")
        
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
