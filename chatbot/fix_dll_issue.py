#!/usr/bin/env python3
"""
DLL Loading Issue Fix Script for JTalk Chatbot
This script fixes the Windows DLL loading issue with PyTorch.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main fix function"""
    print("🔧 JTalk DLL Loading Issue Fix")
    print("=" * 50)
    
    # Step 1: Uninstall all conflicting packages
    print("🗑️  Step 1: Uninstalling conflicting packages...")
    packages_to_remove = [
        'torch',
        'torchvision', 
        'torchaudio',
        'transformers',
        'tokenizers',
        'numpy',
        'tensorflow'
    ]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y", f"Uninstalling {package}")
    
    # Step 2: Install NumPy 1.x first
    print("\n📦 Step 2: Installing NumPy 1.x...")
    if not run_command("pip install numpy==1.24.3", "Installing NumPy 1.24.3"):
        print("❌ NumPy installation failed")
        return False
    
    # Step 3: Install PyTorch CPU-only versions
    print("\n📦 Step 3: Installing PyTorch CPU-only versions...")
    
    # Try CPU-only installation first
    cpu_cmd = "pip install torch==2.0.1+cpu torchvision==0.15.2+cpu torchaudio==2.0.2+cpu --index-url https://download.pytorch.org/whl/cpu"
    
    if run_command(cpu_cmd, "Installing PyTorch CPU-only"):
        print("✅ PyTorch CPU-only installation successful")
    else:
        # Fallback to regular PyPI versions
        print("🔄 Trying fallback PyPI versions...")
        fallback_cmd = "pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2"
        if not run_command(fallback_cmd, "Installing PyTorch fallback"):
            print("❌ PyTorch installation failed")
            return False
    
    # Step 4: Install Transformers
    print("\n📦 Step 4: Installing Transformers...")
    if not run_command("pip install transformers==4.30.2", "Installing Transformers 4.30.2"):
        print("❌ Transformers installation failed")
        return False
    
    # Step 5: Install Tokenizers
    print("\n📦 Step 5: Installing Tokenizers...")
    if not run_command("pip install tokenizers==0.13.3", "Installing Tokenizers 0.13.3"):
        print("❌ Tokenizers installation failed")
        return False
    
    # Step 6: Install other requirements
    print("\n📦 Step 6: Installing other requirements...")
    other_deps = [
        "SpeechRecognition==3.10.0",
        "pyaudio==0.2.11",
        "flask==2.3.3",
        "flask-cors==4.0.0",
        "requests==2.31.0",
        "regex==2023.8.8",
        "tqdm==4.66.1",
        "huggingface-hub==0.16.4",
        "filelock==3.12.4",
        "typing-extensions==4.8.0",
        "packaging==23.2",
        "pyyaml==6.0.1"
    ]
    
    for dep in other_deps:
        run_command(f"pip install {dep}", f"Installing {dep.split('==')[0]}")
    
    # Step 7: Test imports
    print("\n🧪 Step 7: Testing imports...")
    test_imports = [
        ("numpy", "NumPy"),
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("flask", "Flask")
    ]
    
    all_good = True
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} import successful")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            all_good = False
        except Exception as e:
            print(f"❌ {name} import error: {e}")
            all_good = False
    
    if all_good:
        print("\n🎉 All imports successful! Your chatbot should work now.")
        print("🚀 Try running: python chatbot.py")
        return True
    else:
        print("\n❌ Some imports failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n🔧 Manual fix instructions:")
        print("1. pip uninstall numpy torch transformers tokenizers tensorflow -y")
        print("2. pip install numpy==1.24.3")
        print("3. pip install torch==2.0.1+cpu torchvision==0.15.2+cpu torchaudio==2.0.2+cpu --index-url https://download.pytorch.org/whl/cpu")
        print("4. pip install transformers==4.30.2 tokenizers==0.13.3")
        print("5. pip install -r requirements.txt")
    
    input("\nPress Enter to exit...")
