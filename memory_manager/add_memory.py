import json
import os

MEMORY_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory_store.json")

def load_memories():
    if not os.path.exists(MEMORY_FILE_PATH):
        return []
    try:
        with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("memories", [])
    except json.JSONDecodeError:
        return []

def save_memories(memories):
    with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump({"memories": memories}, f, indent=2)

def add_new_memory(new_memory_item):
    current_memories = load_memories()
    
    # Check if key already exists (basic deduplication)
    # In a real system, the 'resolution' step would handle complex logic
    existing_index = -1
    for i, mem in enumerate(current_memories):
        if mem.get("key") == new_memory_item.get("key"):
            existing_index = i
            break
    
    if existing_index != -1:
        print(f"Memory for key '{new_memory_item.get('key')}' already exists. Use update logic.")
        return False
        
    current_memories.append(new_memory_item)
    save_memories(current_memories)
    print(f"Added memory: {new_memory_item.get('key')} = {new_memory_item.get('value')}")
    return True
