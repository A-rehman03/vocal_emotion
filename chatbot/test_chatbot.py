#!/usr/bin/env python3
"""
Test script to debug chatbot issues
"""

import requests
import json
import time

def test_chatbot():
    """Test the chatbot API endpoints"""
    base_url = "http://localhost:5002"
    
    print("🤖 Testing Chatbot API...")
    print("=" * 50)
    
    # Test 1: Check status
    print("1. Checking chatbot status...")
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            status = response.json()
            print("✅ Status:", json.dumps(status, indent=2))
        else:
            print(f"❌ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to chatbot: {e}")
        return
    
    # Test 2: Send test messages
    test_messages = [
        "Hello",
        "How are you?",
        "What can you help me with?",
        "Tell me a joke",
        "What's the weather like?",
        "Help me with something"
    ]
    
    print("\n2. Testing chat responses...")
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: '{message}'")
        try:
            response = requests.post(f"{base_url}/api/chat", 
                                   json={"message": message, "session_id": "test"})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response: {data.get('response', 'No response')}")
            else:
                print(f"❌ Chat failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    # Test 3: Check conversation history
    print("\n3. Checking conversation history...")
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Conversation sessions: {status.get('conversation_sessions', 0)}")
        else:
            print("❌ Could not check conversation history")
    except Exception as e:
        print(f"❌ Error checking history: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_chatbot()
