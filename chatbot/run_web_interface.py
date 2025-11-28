#!/usr/bin/env python3
"""
Web Interface Launcher for JTalk Chatbot
This script starts the web-based chat interface for the chatbot.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask-cors',
        'transformers',
        'torch',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            print("Please install manually: pip install " + " ".join(missing_packages))
            return False
    
    return True

def check_files():
    """Check if required files exist"""
    required_files = [
        'web_server.py',
        'chatbot3.py',
        'intents.json',
        'templates/chat.html'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def start_server():
    """Start the Flask web server"""
    print("🚀 Starting JTalk Web Interface...")
    print("=" * 50)
    
    try:
        # Import and run the web server
        from web_server import app
        
        print("✅ Web server started successfully!")
        print("🌐 Opening browser...")
        
        # Open browser after a short delay
        time.sleep(2)
        webbrowser.open('http://localhost:5002')
        
        print("\n🎉 JTalk is now running!")
        print("📱 Access your chatbot at: http://localhost:5002")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=5002, debug=False)
        
    except KeyboardInterrupt:
        print("\n👋 JTalk stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🤖 JTalk Web Interface Launcher")
    print("=" * 50)
    
    # Change to the chatbot directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check required files
    if not check_files():
        print("❌ Please ensure all required files are present.")
        return
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
