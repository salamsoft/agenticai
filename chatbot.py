import os
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings  # You can use your own embedding model if necessary
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
# Load environment variables (if needed)
load_dotenv()
def load_pdf_data(pdf_folder):
    """Load and extract text from all PDFs in the given folder."""
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    documents = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(os.path.join(pdf_folder, pdf_file))
        documents.extend(loader.load())
    return documents
def create_vector_store(documents):
    """Create a vector store from documents using FAISS."""
    embeddings = OpenAIEmbeddings()  # You can replace this with a local model for offline use
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store
def chatbot(query, vector_store):
    """Handle chatbot query by retrieving relevant context and generating response."""
    llm = ChatOllama(model="llama3")  # Use your Llama model locally
    # Use a retriever to fetch relevant documents from the vector store
    retriever = vector_store.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(llm, retriever)
    response = chain.run(input=query)
    return response
if __name__ == '__main__':
    pdf_folder = 'data'
    documents = load_pdf_data(pdf_folder)
    vector_store = create_vector_store(documents)
    # Save vector store for future use
    vector_store.save_local("data")
    print("Chatbot is ready!")
 
