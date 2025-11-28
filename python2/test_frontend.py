"""
Test script to simulate frontend requests
"""

import requests
import json

def test_predict_endpoint():
    """Test the predict endpoint like the frontend would"""
    url = "http://localhost:5001/predict"
    
    # Test with a sample audio file
    try:
        with open('sad016.wav', 'rb') as audio_file:
            files = {'audio': audio_file}
            response = requests.post(url, files=files)
            
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response: {json.dumps(data, indent=2)}")
                return True
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                return False
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request Error: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    url = "http://localhost:5001/health"
    
    try:
        response = requests.get(url)
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Backend Endpoints...")
    print("=" * 50)
    
    print("\n1. Testing Health Endpoint:")
    health_ok = test_health_endpoint()
    
    print("\n2. Testing Predict Endpoint:")
    predict_ok = test_predict_endpoint()
    
    print("\n" + "=" * 50)
    if health_ok and predict_ok:
        print("✅ All tests passed! Backend is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")

