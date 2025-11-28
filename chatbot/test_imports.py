#!/usr/bin/env python3
"""
Test script to check if all required packages can be imported successfully.
"""

def test_imports():
    """Test all required imports one by one."""
    print("Testing package imports...")
    
    # Test basic imports
    try:
        import os
        import sys
        import json
        import random
        import threading
        import time
        print("✓ Basic Python modules imported successfully")
    except ImportError as e:
        print(f"✗ Error importing basic modules: {e}")
        return False
    
    # Test speech recognition
    try:
        import speech_recognition as sr
        print("✓ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"✗ Error importing SpeechRecognition: {e}")
        return False
    
    # Test PyTorch
    try:
        import torch
        print(f"✓ PyTorch imported successfully (version: {torch.__version__})")
    except ImportError as e:
        print(f"✗ Error importing PyTorch: {e}")
        return False
    except Exception as e:
        print(f"✗ Error loading PyTorch: {e}")
        return False
    
    # Test Transformers
    try:
        from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
        print("✓ Transformers imported successfully")
    except ImportError as e:
        print(f"✗ Error importing Transformers: {e}")
        return False
    except Exception as e:
        print(f"✗ Error loading Transformers: {e}")
        return False
    
    # Test other packages
    try:
        import nltk
        print("✓ NLTK imported successfully")
    except ImportError as e:
        print(f"✗ Error importing NLTK: {e}")
        return False
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Error importing Flask: {e}")
        return False
    
    print("\n🎉 All packages imported successfully!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n✅ Your environment is ready to run the chatbot!")
    else:
        print("\n❌ Please fix the import errors before running the chatbot.")
        print("\nTry these commands:")
        print("pip uninstall torch transformers")
        print("pip install torch==2.6.0+cpu transformers==4.46.0")
