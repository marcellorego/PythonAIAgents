import os
from typing import List

from dotenv import load_dotenv, find_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

AzureOpenAI: str = "Azure"
Ollama: str = "Ollama"

# Load environment variables
load_dotenv(find_dotenv())


def create_azure_chatbot() -> AzureChatOpenAI:
    azure_openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION')
    azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    azure_openai_deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
    model_temperature = os.getenv("MODEL_TEMPERATURE")

    chatbot: AzureChatOpenAI = AzureChatOpenAI(
        azure_endpoint=azure_openai_endpoint,
        azure_deployment=azure_openai_deployment,
        api_version=azure_openai_api_version,
        temperature=model_temperature,
        timeout=120000,  # 2 minutes
        max_retries=2,
    )

    return chatbot


def create_ollama_chatbot() -> ChatOllama:
    ollama_endpoint = os.getenv('OLLAMA_ENDPOINT')
    ollama_model = os.getenv("OLLAMA_MODEL")
    model_temperature = os.getenv("MODEL_TEMPERATURE")
    chatbot: ChatOllama = ChatOllama(
        base_url=ollama_endpoint,
        model=ollama_model,
        temperature=model_temperature,
    )

    return chatbot


def create_chatbot() -> BaseChatModel:
    chatbot_model = os.getenv('CHATBOT_MODEL')
    if chatbot_model == AzureOpenAI:
        return create_azure_chatbot()
    else:
        return create_ollama_chatbot()


def main():
    chatbot: BaseChatModel = create_chatbot()

    messages: List[BaseMessage] = [
        SystemMessage(
            """
            You are an intelligent assistant specialized in Behavior-Driven Development (BDD). Your task is to generate step definitions from BDD scenarios written in Gherkin syntax. The step definitions should be written in {target_language} and utilize the Cucumber framework.

            Requirements:
            
            * Code Quality:
            Ensure that the generated code is clean, well-structured, and adheres to best practices for {target_language} and Cucumber.
            
            * Dependencies:
            Declare and utilize any external references or dependencies required in the step definitions.
            
            * Output Format:
            Do not provide explanations or additional information.
            Only provide output with the complete implementation of the step definitions in {target_language}.
            
            * Input and Output:
            Input: You will receive BDD scenarios written in Gherkin syntax.
            Output: Generate corresponding step definitions in {target_language} using Cucumber. The output should consist solely of code.
            
            * Code Structure:
            Import Given, When, Then dependencies from the Cucumber framework for {target_language}.
            Define step definitions using {target_language} functions.
            Ensure proper type annotations and include error handling where necessary.
            
            Example of Gherkin Scenario:

            ```gherkin
            Feature: User Login
            Scenario: Successful login
              Given the user is on the login page
              When the user enters valid credentials
              Then the user should be redirected to the dashboard
            ```

            * Best Practices:
            Keep step definitions concise and focused on a single responsibility.
            Use meaningful function names to enhance readability.
            Adhere to provided documentation and definitions.
            Handle asynchronous operations appropriately if referenced in documentation.
            """)
    ]

    user_input: str = """
        Given below bdd scenarios written in Gherkin syntax and documentation provided, generate all step definitions in specified language using Cucumber framework.
        
        Gherkin Feature Definitions:
        
        Addition Feature
        Feature: Addition
          Scenario: Add two positive numbers
            Given I have a calculator
            When I add 2 and 3
            Then the result should be 5
        
          Scenario: Add a positive and a negative number
            Given I have a calculator
            When I add 5 and -2
            Then the result should be 3
        
        Subtraction Feature
        Feature: Subtraction
          Scenario: Subtract two positive numbers
            Given I have a calculator
            When I subtract 3 from 5
            Then the result should be 2
        
          Scenario: Subtract a larger number from a smaller number
            Given I have a calculator
            When I subtract 5 from 3
            Then the result should be -2
        
        Multiplication Feature
        Feature: Multiplication
          Scenario: Multiply two positive numbers
            Given I have a calculator
            When I multiply 4 and 3
            Then the result should be 12
        
          Scenario: Multiply a number by zero
            Given I have a calculator
            When I multiply 5 and 0
            Then the result should be 0
        
        Division Feature
        Feature: Division
          Scenario: Divide two positive numbers
            Given I have a calculator
            When I divide 10 by 2
            Then the result should be 5
        
          Scenario: Divide by zero
            Given I have a calculator
            When I divide 10 by 0
            Then an error should be thrown
        
        {target_language} Code Context:
        
        Calculator class is defined in module service/calculator.ts. 
        
        Calculator class has the following methods:

        class Calculator {
            add(a: number, b: number): number {
                return a + b;
            }

            subtract(a: number, b: number): number {
                return a - b;
            }

            multiply(a: number, b: number): number {
                return a * b;
            }

            divide(a: number, b: number): number {
                if (b === 0) {
                    throw new Error("Division by zero is not allowed.");
                }
                return a / b;
            }
        }
        
        Calculator class documentation is described below.
        ---
        
        ### Method: `add`
        
        - **Description**:  
          Calculates the sum of two numbers by adding them together.
        
        - **Parameters**:  
          - **a** (`number`): The first number to be added.  
          - **b** (`number`): The second number to be added.
        
        - **Returns**:  
          - **number**: The sum of `a` and `b`.
        
        - **Usage**:  
          This method is useful for basic arithmetic operations involving addition. Common applications include:
          - Financial calculations (e.g., totaling expenses or revenues).
          - Mathematical computations in algorithms or data analysis.
          - Any scenario requiring the summation of numeric values.
        
        - **Notes**:  
          - Both parameters must be of type `number`. If non-numeric values are passed, the method may produce unexpected results or errors.
        
        --- 
        
        ---
        
        ### Method: `subtract`
        
        - **Description**:  
          Computes the difference between two numbers by subtracting the second number from the first.
        
        - **Parameters**:  
          - **a** (`number`): The minuend, or the number from which another number will be subtracted.  
          - **b** (`number`): The subtrahend, or the number that will be subtracted from `a`.
        
        - **Returns**:  
          - **number**: The result of `a - b`.
        
        - **Usage**:  
          This method is useful for arithmetic operations that require subtraction. Common applications include:
          - Financial calculations (e.g., profit or loss).
          - Statistical analysis (e.g., calculating differences or deviations).
          - Any scenario requiring comparison or adjustment of numeric values.
        
        - **Notes**:  
          - Both parameters must be of type `number`. Passing non-numeric values may lead to unexpected behavior or errors.
        
        ---
        
        ---
        
        ### Method: `multiply`
        
        - **Description**:  
          Computes the product of two numbers by multiplying them together.
        
        - **Parameters**:  
          - **a** (`number`): The first number to be multiplied.  
          - **b** (`number`): The second number to be multiplied.
        
        - **Returns**:  
          - **number**: The product of `a` and `b`.
        
        - **Usage**:  
          This method is useful for arithmetic operations involving multiplication. Common applications include:
          - Calculating total costs in financial scenarios (e.g., price times quantity).
          - Performing mathematical operations in algorithms and data processing.
          - Any scenario requiring the multiplication of numeric values.
        
        - **Notes**:  
          - Both parameters must be of type `number`. Passing non-numeric values may lead to unexpected behavior or errors.
        
        --- 
        
        ---
        
        ### Method: `divide`
        
        - **Description**:  
          Computes the quotient of two numbers by dividing the first number by the second.
        
        - **Parameters**:  
          - **a** (`number`): The numerator, or the number to be divided.  
          - **b** (`number`): The denominator, or the number by which `a` will be divided.
        
        - **Returns**:  
          - **number**: The result of `a / b`.
        
        - **Usage**:  
          This method is essential for performing division operations in various contexts. Common applications include:
          - Financial calculations (e.g., calculating averages or rates).
          - Scientific computations (e.g., determining ratios or proportions).
          - Any scenario requiring the division of numeric values.
        
        - **Notes**:  
          - Both parameters must be of type `number`.
          - The parameter `b` must not be zero, as dividing by zero will result in an error or undefined behavior.
        
        --- 
        
        """

    messages.append(HumanMessage(user_input))

    config = {"configurable": {"target_language": "Python"}}
    ai_response: BaseMessage = chatbot.invoke(messages, config)

    print(ai_response.content)


if __name__ == "__main__":
    main()
