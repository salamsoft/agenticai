import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load FAISS index and query it
def query_vector_database(query, index_path, chunk_path, top_k=5):
    index = faiss.read_index(index_path)
    with open(chunk_path, "rb") as f:
        chunks = pickle.load(f)

    # Embed the query
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = embedding_model.encode([query])

    # Search the FAISS index
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in indices[0]]
