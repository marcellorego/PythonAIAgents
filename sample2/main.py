from langchain.chains.sequential import SimpleSequentialChain
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from typing import List

llm = OllamaLLM(base_url="http://localhost:11434", model="llama3.2", temperature=0)

def simple() -> None:

    messages: List[BaseMessage] = [
        SystemMessage(content="You are an expert data scientist"),
        HumanMessage(content="Write a Python script that trains a neural network on simulated data")
    ]

    responses = llm.invoke(messages)

    print(responses)


def chain() -> None:
    template: str = """
        You are an expert data scientist with expertise in building deep learning models.
        Explain the concept of {concept} in few lines.  
    """

    prompt_1: PromptTemplate = PromptTemplate(
        template=template,
        input_variables=["concept"]
    )

    prompt_2: PromptTemplate = PromptTemplate(
        template="Turn the concept description of {ml_concept} and explain it to me like I am five years old."
    )

    overall_chain = prompt_1 | llm | prompt_2 | llm

    responses = overall_chain.invoke("autoencoder")

    print(responses)


if __name__ == "__main__":
    chain()
