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

def update_existing_memory(new_memory_item):
    current_memories = load_memories()
    
    updated = False
    for i, mem in enumerate(current_memories):
        if mem.get("key") == new_memory_item.get("key"):
            print(f"Updating memory: {mem.get('key')} from '{mem.get('value')}' to '{new_memory_item.get('value')}'")
            current_memories[i] = new_memory_item
            updated = True
            break
            
    if not updated:
        print(f"Memory for key '{new_memory_item.get('key')}' not found. Adding as new.")
        current_memories.append(new_memory_item)
        
    save_memories(current_memories)
    return True
