import faiss
import numpy as np
import pickle
import os


class VectorStore:
    def __init__(self, dim=384, index_path="memory_manager/faiss_index.pkl"):
        self.dim = dim
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(dim)
        self.memory_map = []

        if os.path.exists(index_path):
            self.load_index()

    def rebuild_index(self):
        self.index = faiss.IndexFlatL2(self.dim)

        vectors = []
        for memory in self.memory_map:
            vectors.append(memory["embedding"])

        if vectors:
            vectors_np = np.array(vectors).astype("float32")
            self.index.add(vectors_np)

    def search(self, embedding, top_k=5):
        if self.index.ntotal == 0:
            return []

        vector_np = np.array([embedding]).astype("float32")
        distances, indices = self.index.search(vector_np, top_k)

        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            
            if idx >= len(self.memory_map):
                continue
            
            results.append({
                "memory": self.memory_map[idx]["metadata"],
                "score": float(1 / ( 1 + distance))
            })
        return results

    def save_index(self):
        with open(self.index_path, "wb") as f:
            pickle.dump((self.memory_map,), f)

    def load_index(self):
        with open(self.index_path, "rb") as f:
            (self.memory_map,) = pickle.load(f)

        self.rebuild_index()
