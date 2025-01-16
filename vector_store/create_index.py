from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
import numpy as np
import pickle
from utils.pdf_extractor import extract_text_from_pdf


def create_vector_store(pdf_path, index_path, chunk_path):
    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)

    # Step 3: Generate embeddings
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(chunks)

    # Step 4: Create and save FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    faiss.write_index(index, index_path)

    # Step 5: Save text chunks
    with open(chunk_path, "wb") as f:
        pickle.dump(chunks, f)

    print("Vector store created successfully!")

# Usage
if __name__ == "__main__":
    create_vector_store("data/Vegetables.pdf", "data/local_vector_database.index", "data/document_chunks.pkl")
