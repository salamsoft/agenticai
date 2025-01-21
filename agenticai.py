from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from vector_store.query_index import query_vector_database
import streamlit as st

def chatbot():
    load_dotenv()  # Load environment variables

    # Initialize LangChain and Ollama components
    llm = ChatOllama(model="llama3.2")
    
    # Title of the app
    st.title("Runbook Chatbot 🤖")

    # Initialize chat history in session state if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if user_query := st.chat_input("Ask something about your runbook..."):
        st.chat_message("user").markdown(user_query)
         # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # Prepare a container for the assistant's response
        assistant_message = st.chat_message("assistant")
        response_placeholder = assistant_message.empty()
        
        try:
            context = "\n".join(query_vector_database(
                user_query, "data/local_vector_database.index", "data/document_chunks.pkl"
            ))

            # Prepare the information for the prompt
            information = f"""
            User query: {user_query}
            The attached document is the runbook for our project. Your task is to:
            Understand the structure and content of the runbook.
            Assist SRE and GTS teams by providing quick, accurate, and context-relevant responses based on the runbook's details.
            Simplify navigation by extracting relevant information for troubleshooting incidents, standardizing procedures, and guiding workflows.
            Keep in mind that runbooks are often static, detailed, and challenging to navigate quickly in high-pressure situations. Ensure your responses are concise, actionable, and tailored to the specific query to save time and improve efficiency
            {context}
            """
            
            # Generate a response using LangChain and Ollama with typewriter effect
            response_text = ""  # Accumulate the response text
            for chunk in llm.stream(information):
                if hasattr(chunk, "content"):  # Safely access the chunk content
                    response_text += chunk.content  # Append each chunk's content
                    response_placeholder.markdown(response_text)  # Update the display

            # Add the final assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            error_message = f"Error: {e}"
            response_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
        

if __name__ == "__main__":
    chatbot()

