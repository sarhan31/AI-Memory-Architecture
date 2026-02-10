import json
from memory_manager.memory_engine import MemoryEngine


def run_demo():
    print("=== INITIALIZING MEMORY ENGINE ===")
    engine = MemoryEngine()

    # Step 1: Store initial memories
    sample_memories = {
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
            },
            {
                "type": "preference",
                "key": "notification_preference",
                "value": "email",
                "confidence": 0.88,
                "action": "add"
            },
            {
                "type": "fact",
                "key": "location",
                "value": "Tokyo",
                "confidence": 0.9,
                "action": "add"
            }

        ]
    }

    print("\n=== STORING MEMORIES ===")
    engine.store_memories(sample_memories)
    engine.store_memories(sample_memories)
    

    # Step 2: Test update
    update_memory = {
        "memories": [
            {
                "type": "fact",
                "key": "user_name",
                "value": "Sarah Johnson",
                "confidence": 0.99,
                "action": "update"
            },
            {
                "type": "fact",
                "key": "location",
                "value": "Osaka",
                "confidence": 0.95,
                "action": "update"
            }

        ]
    }

    print("\n=== UPDATING MEMORY (user_name) ===")
    engine.store_memories(update_memory)

    # Step 3: General retrieval
    print("\n=== RETRIEVAL: General Query ===")
    results = engine.retrieve_memories("Suggest dinner options", top_k=5)

    print(json.dumps(results, indent=2))

    # Step 4: Type-filtered retrieval
    print("\n=== RETRIEVAL: Only Constraints ===")
    constraint_results = engine.retrieve_memories(
        "What food should I avoid?",
        memory_type="constraint"
    )
    
    print("\n=== DUPLICATE TEST ===")
    engine.store_memories(sample_memories)
    print(engine.list_all_memories())


    print(json.dumps(constraint_results, indent=2))

    print("\n=== DEMO COMPLETE ===")


if __name__ == "__main__":
    run_demo()
