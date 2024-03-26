"""Using tools with the base OpenAI API.

This example is slightly modified from the OpenAI docs:
https://platform.openai.com/docs/guides/function-calling
"""
import json
from typing import Literal

from openai import OpenAI

from config import Settings

settings = Settings()
client = OpenAI(api_key=settings.openai_api_key)


def get_current_weather(
    location: str, unit: Literal["celsius", "fahrenheit"] = "fahrenheit"
) -> str:
    """Get the current weather in a given location."""
    return f"{location} is 65 degrees {unit}."


# Step 1: send the conversation and available functions to the model
messages = [
    {
        "role": "user",
        "content": "What's the weather like in San Francisco, Tokyo, and Paris?",
    }
]
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit most commonly used in location.",
                    },
                },
                "required": ["location", "unit"],
            },
        },
    }
]
response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=messages,
    tools=tools,
    tool_choice="auto",  # auto is default, but we'll be explicit
)
response_message = response.choices[0].message
tool_calls = response_message.tool_calls
# Step 2: check if the model wanted to call a function
if tool_calls:
    # Step 3: call the function
    # Note: the JSON response may not always be valid; be sure to handle errors
    available_functions = {
        "get_current_weather": get_current_weather,
    }  # only one function in this example, but you can have multiple
    messages.append(response_message)  # extend conversation with assistant's reply
    # Step 4: call each function call and print the output
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )
        print(function_response)
