import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

if __name__ == '__main__':
    load_dotenv()
    print("hello Langchain")

    information = """
    OpenAI is an American artificial intelligence (AI) research organization founded in December 2015 and headquartered in San Francisco, California. Its stated mission is to develop "safe and beneficial" artificial general intelligence (AGI), which it defines as "highly autonomous systems that outperform humans at most economically valuable work".[5] As a leading organization in the ongoing AI boom,[6] OpenAI is known for the GPT family of large language models, the DALL-E series of text-to-image models, and a text-to-video model named Sora.[7][8] Its release of ChatGPT in November 2022 has been credited with catalyzing widespread interest in generative AI.
    """

    summary_template = """
    Given the information {information}, create:
    1. A short summary
    2. Two interesting facts about that
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template
    )

    llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke({"information": information})
    print(res)
