import os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    print("hello Langchain")
    print(os.environ['OPENAI_API_KEY'])