"""Mirascope automatic function conversion for easy function calling with Anthropic."""
from typing import Literal

from mirascope.anthropic import AnthropicCall, AnthropicCallParams

from config import Settings

settings = Settings()


def get_current_weather(
    location: str, unit: Literal["celsius", "fahrenheit"] = "fahrenheit"
) -> str:
    """Get the current weather in a given location."""
    return f"{location} is 65 degrees {unit}."


class Forecast(AnthropicCall):
    prompt_template = "What's the weather like in San Francisco, Tokyo, and Paris?"

    call_params = AnthropicCallParams(tools=[get_current_weather])


response = Forecast().call()
tools = response.tools
if tools:
    for tool in tools:
        print(tool.fn(**tool.args))
