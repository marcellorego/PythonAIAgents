from typing import List
from dotenv import load_dotenv,find_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_community.embeddings import OllamaEmbeddings

from sample3.tools import get_weather

# Load environment variables
load_dotenv(find_dotenv())

# Run basic query with ChatOpenAI wrapper

def translate_test() -> None:

    llm = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3.2",
        temperature=0,
    )


    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that translates {input_language} to {output_language}.",
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    chain.invoke(
        {
            "input_language": "English",
            "output_language": "German",
            "input": "I love programming.",
        }
    )

@tool
def validate_user(user_id: int, addresses: List[str]) -> bool:
    """Validate user using historical addresses.

    Args:
        user_id (int): the user ID.
        addresses (List[str]): Previous addresses as a list of strings.
    """
    return True

def validate_user_test() -> None:

    llm = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3.2",
        temperature=0,
    )

    llm_with_tools = llm.bind_tools([validate_user])

    result = llm_with_tools.invoke(
        "Could you validate user 123? They previously lived at "
        "123 Fake St in Boston MA and 234 Pretend Boulevard in "
        "Houston TX."
    )

    print(result)

def embed_document_test() -> None:

    ollama_emb = OllamaEmbeddings(
        model="nomic-embed-text",
    )
    r1 = ollama_emb.embed_documents(
        [
            "Alpha is the first letter of Greek alphabet",
            "Beta is the second letter of Greek alphabet",
        ]
    )
    print(r1)

    r2 = ollama_emb.embed_query(
        "What is the second letter of Greek alphabet"
    )

    print(r2)


def weather_test() -> None:
    llm = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3.2",
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that have access to the weather of locations.",
            ),
            ("human", "{input}"),
        ]
    )

    chain_with_tools = llm.bind_tools([get_weather])

    chain = prompt | chain_with_tools

    result = chain.invoke({
        "input": "Could you tell me how is the weather in Houston TX?"
    })

    print(result)


# if __name__ == "__main__":
#     weather_test()