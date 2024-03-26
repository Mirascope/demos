"""Using the Mirascope `OpenAITool` class for easier function calling."""
from typing import Literal

from mirascope.base import tool_fn
from mirascope.openai import OpenAICall, OpenAITool, OpenAICallParams
from pydantic import Field

from config import Settings

settings = Settings()


def get_current_weather(
    location: str, unit: Literal["celsius", "fahrenheit"] = "fahrenheit"
) -> str:
    """Get the current weather in a given location."""
    return f"{location} is 65 degrees {unit}."


@tool_fn(get_current_weather)
class GetCurrentWeather(OpenAITool):
    """Get the current weather in a given location."""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")
    unit: Literal["celsius", "fahrenheit"] = "fahrenheit"


class Forecast(OpenAICall):
    prompt_template = "What's the weather like in San Francisco, Tokyo, and Paris?"

    call_params = OpenAICallParams(tools=[GetCurrentWeather])


response = Forecast().call()
tools = response.tools
if tools:
    for tool in tools:
        print(tool.fn(**tool.args))
