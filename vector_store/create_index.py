import os
import faiss
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pdfplumber

def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text()
    return all_text

def create_vector_store(directory_path, index_path, chunk_path):
    all_texts = []  # To store extracted text from all files

    # Iterate over all PDF files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):  # Process only PDF files
            file_path = os.path.join(directory_path, filename)
            print(f"Processing: {file_path}")

            # Extract text from the current file
            extracted_text = extract_text_from_pdf(file_path)
            all_texts.append(extracted_text)

    # Combine all texts into a single string
    combined_text = "\n".join(all_texts)

    # Split the combined text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(combined_text)

    # Generate embeddings for each chunk
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(chunks)

    # Create and save the FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, index_path)

    # Save the chunks to a file
    with open(chunk_path, "wb") as f:
        pickle.dump(chunks, f)

    print("Vector store created successfully!")

if __name__ == "__main__":
    create_vector_store("data/", "data/local_vector_database.index", "data/document_chunks.pkl")