import time
from memory_manager.embedding_service import generate_embedding
from memory_manager.vector_store import VectorStore


class MemoryEngine:
    """
    MemoryEngine handles:
    - Structured memory storage
    - Embedding generation
    - Vector indexing using FAISS
    - Similarity-based retrieval
    - Optional filtering by memory type
    """

    def __init__(self):
        self.store = VectorStore()

    def _memory_exists(self, key, value):
        for item in self.store.memory_map:
            if item["metadata"]["key"] == key and item["metadata"]["value"] == value:
                return True
        return False

    def _remove_existing_key(self, key):
        self.store.memory_map = [
            item for item in self.store.memory_map
            if item["metadata"]["key"] != key
        ]
        self.store.rebuild_index()

    def store_memories(self, memory_json):
        updated = False
        
        for memory in memory_json.get("memories", []):

            key = memory["key"]
            value = memory["value"]
            action = memory["action"]

            if action == "update":
                self._remove_existing_key(key)
                updated = True

            if self._memory_exists(key, value):
                continue  # Skip duplicate

            text_representation = f"{memory['type']} | {key} | {value}"
            embedding = generate_embedding(text_representation)

            self.store.memory_map.append({
                "metadata": memory,
                "embedding": embedding
            })

            updated = True
            
        if updated:
            self.store.rebuild_index()
            self.store.save_index()

    def retrieve_memories(self, query_text, top_k=5, score_threshold=3.0, memory_type=None):
        start_time = time.time()

        query_embedding = generate_embedding(query_text)
        raw_results = self.store.search(query_embedding, top_k)
        
        filtered_results = []
        
        for result in raw_results:
            if result['score'] > score_threshold:
                continue
            
            if memory_type and result["memory"]["type"] != memory_type:
                continue
            
            filtered_results.append(result)

        latency = time.time() - start_time
        print(f"[MemoryEngine] Retrieval latency: {latency:.4f} seconds")
        print(f"[MemoryEngine] Returned {len(filtered_results)} relevant memories")
        print(f"[MemoryEngine] Total memories stored: {len(self.store.memory_map)}")

        return filtered_results
    
    def list_all_memories(self):
        """
        Return all stored memories (debug / inspection use).
        """
        return [item["metadata"] for item in self.store.memory_map]

