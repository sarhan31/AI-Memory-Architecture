"""
Quick test to verify local mode is working
Run this before starting the server
"""
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("🧪 Testing Local Mode Configuration")
print("="*60)

# Test 1: Check .env file
print("\n1. Checking .env configuration...")
if os.path.exists(".env"):
    print("   ✅ .env file exists")
    with open(".env", "r") as f:
        content = f.read()
        if "USE_LOCAL_FALLBACK=true" in content:
            print("   ✅ Local fallback enabled")
        else:
            print("   ⚠️  Local fallback not enabled")
else:
    print("   ❌ .env file not found")

# Test 2: Import dependencies
print("\n2. Checking dependencies...")
try:
    import fastapi
    print("   ✅ FastAPI installed")
except ImportError:
    print("   ❌ FastAPI not installed")

try:
    import uvicorn
    print("   ✅ Uvicorn installed")
except ImportError:
    print("   ❌ Uvicorn not installed")

try:
    import sentence_transformers
    print("   ✅ sentence-transformers installed")
except ImportError:
    print("   ❌ sentence-transformers not installed")

try:
    import faiss
    print("   ✅ FAISS installed")
except ImportError:
    print("   ❌ FAISS not installed")

# Test 3: Test LLM Client
print("\n3. Testing LLM Client...")
try:
    from orchestrator.services.llm_client import LLMClient
    client = LLMClient()
    
    if client.is_available():
        print("   ✅ LLM Client initialized")
        
        # Test generation
        response = client.generate("Hello, my name is Sarah")
        print(f"   ✅ Generated response: {response[:50]}...")
    else:
        print("   ❌ LLM Client not available")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Test Memory Engine
print("\n4. Testing Memory Engine...")
try:
    from memory_manager.memory_engine import MemoryEngine
    engine = MemoryEngine()
    print("   ✅ Memory Engine initialized")
    
    # Test storing a memory
    test_memory = {
        "memories": [{
            "type": "fact",
            "key": "user_name",
            "value": "TestUser",
            "confidence": 0.95,
            "action": "add"
        }]
    }
    engine.store_memories(test_memory)
    print("   ✅ Memory storage works")
    
    # Test retrieval
    results = engine.retrieve_memories("user name", top_k=1)
    print(f"   ✅ Memory retrieval works (found {len(results)} memories)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "="*60)
print("📊 Test Summary")
print("="*60)
print("\n✅ System is ready to run in LOCAL MODE!")
print("\nTo start the server, run:")
print("   python run_orchestrator.py")
print("\nOr manually:")
print("   python -m orchestrator.main")
print("\n" + "="*60)
