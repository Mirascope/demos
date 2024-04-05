"""Extract JSON from a webpage using natural language"""

from typing import Literal, Type
from urllib.request import Request, urlopen

import weave
from bs4 import BeautifulSoup
from fastapi import FastAPI
from mirascope.anthropic import AnthropicCallParams, AnthropicExtractor
from mirascope.base.tools import DEFAULT_TOOL_DOCSTRING
from mirascope.openai import OpenAIExtractor
from mirascope.wandb import with_weave
from pydantic import BaseModel, Field, computed_field, create_model

from config import Settings

settings = Settings()
app = FastAPI()


weave.init("ploomber-demo")


class FieldDefinition(BaseModel):
    """Define the fields to extract from the webpage."""

    name: str = Field(..., description="The desired name for this field.")
    type: Literal["str", "int", "float", "bool"]


@with_weave
class SchemaGenerator(OpenAIExtractor[list[FieldDefinition]]):
    """Generate a schema based on a user query."""

    api_key = settings.openai_api_key

    extract_schema: Type[list] = list[FieldDefinition]

    prompt_template = """
    Call your tool with field definitions based on this query:
    {query}
    """

    query: str


@with_weave
class WebpageURLExtractor(AnthropicExtractor[BaseModel]):
    """Extract JSON from a webpage using natural language"""

    api_key = settings.anthropic_api_key

    extract_schema: Type[BaseModel] = BaseModel

    prompt_template = """
    YOU MUST USE THE PROVIDED TOOL FUNCTION.
    Call the function with parameters extracted from the following content:
    {webpage_content}
    """

    url: str
    query: str

    call_params = AnthropicCallParams(max_tokens=4000)

    @computed_field
    @property
    def webpage_content(self) -> str:
        """Returns the text content of the webpage found at `url`."""
        request = Request(url=self.url, headers={"User-Agent": "Mozilla/6.0"})
        html_doc = urlopen(request).read().decode("utf-8")
        soup = BeautifulSoup(html_doc, "html.parser")
        text = soup.get_text()
        for link in soup.find_all("a"):
            text += f"\n{link.get('href')}"
        return text

    def generate_schema(self) -> None:
        """Sets `extract_schema` to a schema generated based on `query`."""
        field_definitions = SchemaGenerator(query=self.query).extract()
        model = create_model(
            "ExtractedFields",
            __doc__=DEFAULT_TOOL_DOCSTRING,
            **{
                field.name.replace(" ", "_"): (field.type, ...)
                for field in field_definitions
            },
        )
        self.extract_schema = list[model]


@app.post("/extract")
def extract(
    extractor: WebpageURLExtractor,
) -> list[dict[str, str | int | bool | float]]:
    """Extract JSON from a webpage using natural language"""
    extractor.generate_schema()
    return [model.model_dump() for model in extractor.extract()]
