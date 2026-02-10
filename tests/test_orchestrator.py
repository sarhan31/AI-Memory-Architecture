"""
Test script for the orchestrator API
Run the server first: python -m orchestrator.main
Then run this test: python tests/test_orchestrator.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_chat():
    """Test chat endpoint"""
    print("\n=== Testing Chat Endpoint ===")
    
    # First message
    payload = {
        "user_id": "test_user_123",
        "message": "Hi, I'm Sarah and I live in Tokyo. I prefer email notifications."
    }
    
    response = requests.post(f"{BASE_URL}/chat/", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Second message (should use memory)
    payload2 = {
        "user_id": "test_user_123",
        "message": "What's my name and where do I live?"
    }
    
    print("\n--- Second message (with memory context) ---")
    response2 = requests.post(f"{BASE_URL}/chat/", json=payload2)
    print(f"Status: {response2.status_code}")
    print(f"Response: {json.dumps(response2.json(), indent=2)}")
    
    return response.status_code == 200 and response2.status_code == 200


def test_memory_retrieval():
    """Test memory retrieval endpoint"""
    print("\n=== Testing Memory Retrieval Endpoint ===")
    
    payload = {
        "user_id": "test_user_123",
        "query": "user preferences",
        "top_k": 5
    }
    
    response = requests.post(f"{BASE_URL}/chat/retrieve", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_metrics():
    """Test metrics endpoint"""
    print("\n=== Testing Metrics Endpoint ===")
    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


if __name__ == "__main__":
    print("Starting Orchestrator API Tests...")
    print("Make sure the server is running: python -m orchestrator.main")
    
    try:
        # Run tests
        results = {
            "health": test_health(),
            "chat": test_chat(),
            "memory_retrieval": test_memory_retrieval(),
            "metrics": test_metrics()
        }
        
        # Summary
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        for test_name, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        print("\n" + ("🎉 All tests passed!" if all_passed else "⚠️ Some tests failed"))
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server.")
        print("Please start the server first: python -m orchestrator.main")
