from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    """
    Generate embedding locally using sentence-transformers.
    """
    embedding = model.encode(text)
    return embedding.tolist()
