from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from vector_store.query_index import query_vector_database
def chatbot():
    load_dotenv()  # Load environment variables

    # Initialize LangChain and Ollama components
    llm = ChatOllama(model="llama3.2")

    # Start an interactive chatbot loop
    print("Welcome to the Runbook Chatbot! Type 'exit' to quit.")
    while True:
        # Take user input
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Retrieve relevant context from the vector database
        try:
            context = "\n".join(query_vector_database(
                user_query, "data/local_vector_database.index", "data/document_chunks.pkl"
            ))

            # Prepare the information for the prompt
            information = f"""
            User query: {user_query}
            Context from the database:
            {context}
            """

            # Generate a response using LangChain and Ollama
            response = llm.invoke(information).content

            # Print the chatbot response
            print(f"Chatbot: {response}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chatbot()