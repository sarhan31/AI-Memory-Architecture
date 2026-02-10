import json
from memory_manager.memory_engine import MemoryEngine

# Create engine
engine = MemoryEngine()

# Simulated extracted memory (from extractor layer)
sample_memory = {
    "memories": [
        {
            "type": "fact",
            "key": "user_name",
            "value": "Sarah",
            "confidence": 0.95,
            "action": "add"
        },
        {
            "type": "constraint",
            "key": "dietary_restriction",
            "value": "no peanuts",
            "confidence": 0.90,
            "action": "add"
        }
    ]
}

print("Storing memories...")
engine.store_memories(sample_memory)

print("Retrieving relevant memory for query...")
results = engine.retrieve_memories("Suggest dinner options")

print("\nRetrieved Memories:")
print(json.dumps(results, indent=2))
