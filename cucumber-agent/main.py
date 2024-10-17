import os
from typing import List

from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI

# Load environment variables
load_dotenv(find_dotenv())

def main():
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')

    chatbot: AzureChatOpenAI = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION,
        temperature=0.0,
        timeout=120000,  # 2 minutes
        max_retries=2,
    )

    messages: List[BaseMessage] = [
        SystemMessage(
            """
            You are an intelligent assistant specialized in Behavior-Driven Development (BDD). 
            Your task is to generate step definitions from BDD scenarios written in Gherkin syntax. 
            The step definitions should be written in {target_language} and use the Cucumber framework. 
            Ensure that the generated code is clean, well-structured, and follows best practices for {target_language} and Cucumber.
            Do not explain the process or provide additional information.

            Instructions:
            
            Input: You will receive BDD scenarios written in Gherkin syntax.
            Output: Generate corresponding step definitions in {target_language} using Cucumber.
            Code Structure:
            Use import { Given, When, Then } for importing Cucumber functions.
            Define step definitions using {target_language} functions.
            Ensure proper type annotations and error handling.
            Example: Gherkin Scenario:
            Feature: User Login
            
            Scenario: Successful login
              Given the user is on the login page
              When the user enters valid credentials
              Then the user should be redirected to the dashboard
            
            Best Practices:
            Use asynchronous operations when possible.
            Keep step definitions concise and focused on a single responsibility.
            Use meaningful function names and comments to enhance readability.
            """)
    ]


    user_input: str = """
        Given below bdd scenarios and code context provided, generate all step definitions in {target_language} using Cucumber.
        
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
        The class has the following methods:
        
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
        
        """

    messages.append(HumanMessage(user_input))

    config = {"configurable": {"target_language": "TypeScript"}}
    ai_response: BaseMessage = chatbot.invoke(messages, config)

    print(ai_response.content)

if __name__ == "__main__":
    main()
