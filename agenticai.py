

# from dotenv import load_dotenv
# from langchain.prompts import PromptTemplate
# from langchain_ollama import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
# from vector_store.query_index import query_vector_database

# if __name__ == "__main__":
#     load_dotenv()

#     # User query
#     user_query = "What is the definition of a vegetable?"

#     # Retrieve relevant context from vector database
#     context = "\n".join(query_vector_database(
#         user_query, "data/local_vector_database.index", "data/document_chunks.pkl"
#     ))

#     # Prepare the prompt
#     information = f"""
#     User query: {user_query}
#     Context: {context}
#     """

#     # Use LangChain prompt template
#     summary_template = """
#     Given the information {information}, create:
#     1. A short summary.
#     2. Two interesting facts about it.
#     """

#     summary_prompt_template = PromptTemplate(
#         input_variables=["information"],
#         template=summary_template
#     )

#     llm = ChatOllama(model="llama3.2")
#     chain = summary_prompt_template | llm | StrOutputParser()

#     res = chain.invoke({"information": information})
#     print(res)


# from dotenv import load_dotenv
# from langchain.prompts import PromptTemplate
# from langchain_ollama import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
 
# if __name__ == '__main__':
#     load_dotenv()
 
#     information = """
#     New York
#     """
 
#     summary_template = """
#     Given the information {information}, create:
#     1. A short summary
#     2. Two interesting facts about that
#     """
 
#     summary_prompt_template = PromptTemplate(
#         input_variables=["information"],
#         template=summary_template
#     )
 
#     llm = ChatOllama(model="llama3.2")
 
#     chain = summary_prompt_template | llm | StrOutputParser()
#     res = chain.invoke({"information": information})
#     print(res)



# import ollama

# from vector_store.query_index import query_vector_store

# def chatbot():
#     print("Welcome to the Vegetable Chatbot!")
#     while True:
#         user_query = input("You: ")
#         if user_query.lower() in ["exit", "quit"]:
#             print("Goodbye!")
#             break
        
#         # Query the vector store
#         results = query_vector_store(user_query, "data/local_vector_database.index", "data/document_chunks.pkl")

#         # Prepare context
#         context = "\n".join(results)

#         # Generate response using Ollama
#         try:
#             response = ollama.chat(model="llama3.2", input=f"Context: {context}\n\nUser: {user_query}\nChatbot:")
#             print(f"Chatbot: {response}")
#         except Exception as e:
#             print(f"Error: {e}")

# if __name__ == "__main__":
#     chatbot()

import streamlit as st
from chatbot import chatbot, create_vector_store, load_pdf_data
from langchain.vectorstores import FAISS

# Load the vector store (from saved file)
vector_store = FAISS.load_local("data/local_vector_database.index")

st.title("Runbook Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_response(query):
    """Fetch response from the chatbot."""
    response = chatbot(query, vector_store)
    return response

# Display previous messages
for message in st.session_state.messages:
    st.markdown(f"**{message['role']}**: {message['content']}")

# Get user input
user_input = st.text_input("Ask me something:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get chatbot's response
    bot_response = get_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Display the response
    st.markdown(f"**Bot**: {bot_response}")