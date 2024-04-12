from typing import List, Type

from mirascope.openai import OpenAIExtractor
from pydantic import BaseModel

prev_revision_id = None
revision_id = "0001"


class QueryTemplateList(BaseModel):
    queries: List[str]
    templated_variables: List[str]


class QueryTemplateListExtractor(OpenAIExtractor[QueryTemplateList]):
    """Generates a list of queries and the set of Templated Variables that are present in all of the lists in one call from a given string of the list.
    Doing in one call saves latency and input tokens."""

    extract_schema: Type[QueryTemplateList] = QueryTemplateList
    prompt_template = """
    Extract the query template list from the following text:
    {unextracted_query_list}
    """

    unextracted_query_list: str
