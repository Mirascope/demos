from typing import List, Type

from mirascope.openai import OpenAICallParams, OpenAIExtractor
from pydantic import BaseModel


class TemplateVariableOptions(BaseModel):
    """A Model to hold a list of potential template variables to be used later in potential synthetic queries."""

    options: List[str]


class TemplateVariableListGeneratorAndExtractor(
    OpenAIExtractor[TemplateVariableOptions]
):
    """Generates and extracts potential variables to substitute in for our Template variables. Does the generation and outputs/extracts into a specified format in one API call.
    There might be some Validation errors, best to run in a try-catch setup."""

    extract_schema: Type[TemplateVariableOptions] = TemplateVariableOptions
    prompt_template = """
    You are given a template variable.
    Respond with a list of potential values for that template vairable, in the context of {library_focus}.
    However, they need to be in the format of TemplateCariableOptions, with the template variable associated with the list.
    Try to give 5 real options, but if you can't think of 5 give as many as you can.
    This response needs to be directly extractable into a pydantic model, with no validation errors.
    {template_variable}
    """

    template_variable: str
    library_focus: str
    call_params = OpenAICallParams(model="gpt-4-0125-preview")


class TemplateVariableListExtractorOnly(OpenAIExtractor[TemplateVariableOptions]):
    """Extracts potential variables to substitue in for our Template Variables. Useful for using with smaller models who cannot generate structured information as strongly."""

    extract_schema: Type[TemplateVariableOptions] = TemplateVariableOptions
    prompt_template = """
    Extract a TemplateVariableOptions Model from the following list:
    {extraction_list_str}
    
    """

    extraction_list_str: str
    call_params = OpenAICallParams(model="gpt-4-0125-preview")
