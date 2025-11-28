#!/usr/bin/env python3
"""
PyTorch Setup Fix Script for JTalk Chatbot
This script fixes the DLL loading issue with PyTorch on Windows.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_system():
    """Check system information"""
    print("🖥️  System Information:")
    print(f"   Platform: {platform.platform()}")
    print(f"   Python: {sys.version}")
    print(f"   Architecture: {platform.architecture()}")
    print("=" * 50)

def uninstall_conflicting_packages():
    """Uninstall conflicting PyTorch packages"""
    packages_to_remove = [
        'torch',
        'torchvision', 
        'torchaudio',
        'transformers',
        'tokenizers'
    ]
    
    print("🗑️  Removing conflicting packages...")
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y", f"Uninstalling {package}")

def install_pytorch_cpu():
    """Install PyTorch CPU-only version"""
    print("📦 Installing PyTorch CPU-only version...")
    
    # Try CPU-only version first
    pytorch_cmd = "pip install torch==2.0.1+cpu torchvision==0.15.2+cpu torchaudio==2.0.2+cpu --index-url https://download.pytorch.org/whl/cpu"
    
    if run_command(pytorch_cmd, "Installing PyTorch CPU"):
        return True
    else:
        # Fallback to regular PyPI versions
        print("🔄 Trying fallback PyPI versions...")
        fallback_cmd = "pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2"
        return run_command(fallback_cmd, "Installing PyTorch fallback")

def install_other_dependencies():
    """Install other required dependencies"""
    dependencies = [
        "transformers==4.30.2",
        "tokenizers==0.13.3",
        "numpy==1.24.3",
        "flask==2.3.3",
        "flask-cors==4.0.0",
        "SpeechRecognition==3.10.0",
        "requests==2.31.0",
        "safetensors==0.3.3"
    ]
    
    print("📦 Installing other dependencies...")
    for dep in dependencies:
        run_command(f"pip install {dep}", f"Installing {dep.split('==')[0]}")

def test_imports():
    """Test if imports work correctly"""
    print("🧪 Testing imports...")
    
    test_imports = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("flask", "Flask"),
        ("numpy", "NumPy")
    ]
    
    all_good = True
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} import successful")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            all_good = False
    
    return all_good

def main():
    """Main setup function"""
    print("🤖 JTalk PyTorch Setup Fix")
    print("=" * 50)
    
    check_system()
    
    # Step 1: Uninstall conflicting packages
    uninstall_conflicting_packages()
    
    # Step 2: Install PyTorch CPU version
    if not install_pytorch_cpu():
        print("❌ PyTorch installation failed. Please try manual installation.")
        return False
    
    # Step 3: Install other dependencies
    install_other_dependencies()
    
    # Step 4: Test imports
    if test_imports():
        print("🎉 All imports successful! Your chatbot should work now.")
        print("🚀 Try running: python chatbot.py")
        return True
    else:
        print("❌ Some imports failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🔧 Manual fix instructions:")
        print("1. pip uninstall torch transformers tokenizers")
        print("2. pip install torch==2.0.1+cpu torchvision==0.15.2+cpu torchaudio==2.0.2+cpu --index-url https://download.pytorch.org/whl/cpu")
        print("3. pip install transformers==4.30.2")
        print("4. pip install -r requirements.txt")
    
    input("\nPress Enter to exit...")
