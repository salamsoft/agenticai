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


# import faiss
# import pickle
# import numpy as np
# from sentence_transformers import SentenceTransformer

# def query_vector_store(query, index_path, chunk_path, k=5):
#     # Load the FAISS index and text chunks
#     index = faiss.read_index(index_path)
#     with open(chunk_path, "rb") as f:
#         chunks = pickle.load(f)

#     # Embed the query
#     embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
#     query_embedding = embedding_model.encode([query])

#     # Search the index
#     distances, indices = index.search(np.array(query_embedding), k)

#     # Retrieve matching chunks
#     results = [chunks[i] for i in indices[0]]
#     return results

# # Usage
# if __name__ == "__main__":
#     query = "What is the definition of a vegetable?"
#     results = query_vector_store(query, "data/local_vector_database.index", "data/document_chunks.pkl")
#     for i, result in enumerate(results, 1):
#         print(f"Result {i}:\n{result}\n")