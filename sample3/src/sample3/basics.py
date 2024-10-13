from dotenv import load_dotenv,find_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv(find_dotenv())

# Run basic query with ChatOpenAI wrapper

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3.2",
    temperature=0,
)

output_parser = StrOutputParser()

## Example of a ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

chain = prompt | llm | output_parser

result = chain.invoke({
    "name": "Smith",
    "user_input": "What is your name?"
})
print(result)

# print("input_schema", chain.input_schema.schema())
# print("output_schema", chain.output_schema.schema())


french_german_prompt = ChatPromptTemplate.from_messages([
    ("human", "Please tell me the french and german words for {word} with an example sentence for each.")
])


french_german_chain = french_german_prompt | llm | output_parser

result = french_german_chain.invoke({"word": "polar bear"})
print(result)

check_if_correct_prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant that looks at a question and its given answer. 
    You will find out what is wrong with the answer and improve it. 
    You will return the improved version of the answer.
    Question:
    {question}
    Answer Given:
    {initial_answer}
    Review the answer and give me an improved version instead.
    Improved answer:
    """
)

check_answer_chain = check_if_correct_prompt | llm | output_parser


def run_chain(word: str) -> str:
    initial_answer = french_german_chain.invoke({"word": word})
    print("initial answer:", initial_answer, end="\n\n")
    answer = check_answer_chain.invoke(
        {
            "question": f"Please tell me the french and german words for {word} with an example sentence for each.",
            "initial_answer": initial_answer,
        }
    )
    print("improved answer:", answer)
    return answer

run_chain("strawberries")