import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Load the PDF and extract text
pdf_path = "database/ReleaseGuide.pdf"
all_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        all_text += page.extract_text()

# print(all_text[:500])  # Display the first 500 characters to confirm

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_text(all_text)

# Load a local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings for the text chunks
embeddings = embedding_model.encode(chunks)
