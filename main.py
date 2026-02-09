import os
import json
from extractor.extract_memory import extract_memory_from_chat
from memory_manager.add_memory import add_new_memory
from memory_manager.update_memory import update_existing_memory
from memory_manager.deduplicate import deduplicate_memories

def main():
    print("Starting Memory Architecture Pipeline...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chat_path = os.path.join(base_dir, "tests", "simulated_chat.json")
    prompt_path = os.path.join(base_dir, "prompts", "memory_prompt.txt")
    
    # 1. Extraction
    print(f"Reading chat from {chat_path}")
    extraction_result = extract_memory_from_chat(chat_path, prompt_path)
    
    extracted_memories = extraction_result.get("memories", [])
    print(f"Extracted {len(extracted_memories)} potential memories.")
    
    if not extracted_memories:
        print("No memories extracted.")
        return

    # 2. Resolution & Storage
    # In a full system, we would compare with existing memories using resolution_prompt.
    # Here we simulate the decision logic based on the 'action' field from extraction.
    
    for mem in extracted_memories:
        action = mem.get("action")
        
        if action == "add":
            add_new_memory(mem)
        elif action == "update":
            update_existing_memory(mem)
        else:
            print(f"Unknown action '{action}' for key '{mem.get('key')}'")
            
    print("\nPipeline completed successfully.")
    
    # Display final state
    memory_store_path = os.path.join(base_dir, "memory_store.json")
    if os.path.exists(memory_store_path):
        print("\nFinal Memory Store Content:")
        with open(memory_store_path, 'r', encoding='utf-8') as f:
            print(f.read())

if __name__ == "__main__":
    main()
