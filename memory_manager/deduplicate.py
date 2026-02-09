import json
import os

def deduplicate_memories(memories):
    """
    Simple deduplication based on key.
    Keeps the last occurrence if duplicates exist.
    """
    seen_keys = set()
    unique_memories = []
    
    # Process in reverse to keep the latest
    for mem in reversed(memories):
        key = mem.get("key")
        if key and key not in seen_keys:
            seen_keys.add(key)
            unique_memories.append(mem)
            
    return list(reversed(unique_memories))

if __name__ == "__main__":
    # Test
    test_data = [
        {"key": "a", "value": "1"},
        {"key": "b", "value": "2"},
        {"key": "a", "value": "3"}
    ]
    print(deduplicate_memories(test_data))
