from typing import List

from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import ToolMessage, BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama

from tools import get_weather

# Load environment variables
load_dotenv(find_dotenv())

# If the AI decided to invoke a tool, invoke it
available_functions = {
    "get_weather": get_weather
}


def prompt_ai(chatbot_with_tools: Runnable, messages: List[BaseMessage], nested_calls=0) -> AIMessage:
    if nested_calls > 5:
        raise "AI is tool calling too much!"

    ai_response = chatbot_with_tools.invoke(messages)

    tool_calls = len(ai_response.tool_calls) > 0

    # Second, see if the AI decided it needs to invoke a tool
    if tool_calls:

        # Add the tool request to the list of messages so the AI knows later it invoked the tool
        messages.append(ai_response)

        # Next, for each tool the AI wanted to call, call it and add the tool result to the list of messages
        for tool_call in ai_response.tool_calls:
            tool_name = tool_call["name"].lower()
            selected_tool = available_functions[tool_name]
            tool_output = selected_tool.invoke(tool_call["args"])
            messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

        # Call the AI again so it can produce a response with the result of calling the tool(s)
        ai_response = prompt_ai(chatbot_with_tools, messages, nested_calls + 1)

    return ai_response


def main():
    # First, prompt the AI with the latest user message
    tools = [get_weather]

    chatbot = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3.2",
        temperature=0)
    chatbot_with_tools: Runnable = chatbot.bind_tools(tools)

    messages: List[BaseMessage] = [
        SystemMessage(
            "You are a helpful assistant that have access to the weather of locations. \
                       If user requires to know the weather from any location, use any tool you have to figure it out. \
                       Otherwise, just answer appropriate answer back ")
    ]

    while True:
        user_input = input("Chat with AI (q to quit): ").strip()

        if user_input == 'q':
            break

        messages.append(HumanMessage(user_input))
        ai_response: AIMessage = prompt_ai(chatbot_with_tools, messages)

        print(ai_response.content)
        messages.append(ai_response)


if __name__ == "__main__":
    main()
