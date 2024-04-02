from mirascope.openai import OpenAICall, OpenAICallParams, OpenAIExtractor
from mirascope.anthropic import AnthropicCall, AnthropicCallParams
from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Type

class SyntheticQueryGenerationPrompt(OpenAICall):
    """Generates a series of potential code-based prompts for a downstream language model, based upon a specific library and tasks, plus a prompt-generation strategy."""
    prompt_template = """
    SYSTEM: 
    You are an excellent programmer, and prompt engineer for prompting Large Language Models to recieve the outputs that you are asked to create. 
    You are also very experienced and talented at creating synthetic datasets from large language models, and the strategies to create those datasets with Language Models.

    USER: 
    I'm looking to create a set of synthetic <Queries, Response> pairs. 
    The queries will be asking for asking the model to provide code for tasks using {library_focus} to perform {task_type} tasks that users might want done from the command line. 
    The answers will be the answers to those queries. For right now, we specifically care about the synthetic queries.
    To generate this query, we will be using the {generation_strategy} strategy, where you need to: {generation_strategy_description}

    Here are some example(s):
    {few_shot_examples}
    Generate a very diverse set of {num_results} examples like this, but keep the format the same.
    The diversity is key as we will need to scale this dataset to thousands of samples.

    """

    library_focus : str
    task_type : str
    generation_strategy : str
    generation_strategy_description : str
    examples : List[str]
    num_results : int

    call_params = OpenAICallParams(model="gpt-4")


    @property
    def few_shot_examples(self) -> str:
        examples_string = ""
        for example in self.examples:
            examples_string = examples_string + example + "\n"

        print(examples_string)
        return examples_string

class QueryTemplateList(BaseModel):
    queries : List[str]
    templated_variables : List[str]

class QueryTemplateListExtractor(OpenAIExtractor[QueryTemplateList]):
    """Generates a list of queries and the set of Templated Variables that are present in all of the lists in one call from a given string of the list. 
    Doing in one call saves latency and input tokens."""
    extract_schema: Type[QueryTemplateList] = QueryTemplateList
    prompt_template = """
    Extract the query template list from the following text:
    {unextracted_query_list}
    """

    unextracted_query_list : str


class TemplateVariableOptions(BaseModel):
    options: List[str]

class TemplateVariableListGeneratorAndExtractor(OpenAIExtractor[TemplateVariableOptions]):
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

    template_variable : str
    library_focus : str
    call_params = OpenAICallParams(model = "gpt-4-0125-preview")

class TemplateVariableListExtractorOnly(OpenAIExtractor[TemplateVariableOptions]):
    """Extracts potential variables to substitue in for our Template Variables. Useful for using with smaller models who cannot generate structured information as strongly."""
    extract_schema: Type[TemplateVariableOptions] = TemplateVariableOptions
    prompt_template ="""
    Extract a TemplateVariableOptions Model from the following list:
    {extraction_list_str}

    """
    extraction_list_str : str
    call_params = OpenAICallParams(model = "gpt-4-0125-preview")
