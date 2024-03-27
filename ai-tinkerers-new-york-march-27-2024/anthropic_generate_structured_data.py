"""Generating structured data using Claude Haiku."""
from typing import Type

from mirascope.anthropic import AnthropicCallParams, AnthropicExtractor
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str


class ReviewGenerator(AnthropicExtractor[list[Book]]):
    extract_schema: Type[list] = list[Book]
    prompt_template = """
    SYSTEM:
    Your task is to generate a list of `Book` tool calls.
    You must use the tool to generate them.

    USER:
    Generate 3 {genre} books you think I should read.
    """

    genre: str

    call_params = AnthropicCallParams(model="claude-3-haiku-20240307")


books = ReviewGenerator(genre="science fiction").extract()
for book in books:
    print(book)
