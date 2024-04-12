from typing import List

from mirascope import tags
from mirascope.openai import OpenAICall, OpenAICallParams

prev_revision_id = None
revision_id = "0001"


@tags(["version:0001"])
class SyntheticQueryGenerationPrompt(OpenAICall):
    """Generates a series of potential code-based prompts for a downstream language model, based upon a specific library and tasks, plus a prompt-generation strategy."""

    prompt_template = """
    SYSTEM:
    You are an excellent programmer, and prompt engineer for prompting Large Language Models to recieve the outputs that you are asked to create.
    You are also very experienced and talented at creating synthetic datasets from large language models, and the strategies to create those datasets with Language Models.
    
    USER:
    I'm looking to create a set of synthetic <Queries, Response> pairs.
    The queries will be asking the model to provide code for tasks using {library_focus} to perform {task_type} tasks that users might want done from the command line.
    The answers will be the answers to those queries. For right now, we specifically care about the synthetic queries.
    To generate this query, we will be using the {generation_strategy} strategy, where you need to: {generation_strategy_description}
    
    Here are some example(s):
    {few_shot_examples}
    Generate a very diverse set of {num_results} examples like this, but keep the format the same.
    The diversity is key as we will need to scale this dataset to thousands of samples.
    
    """

    library_focus: str
    task_type: str
    generation_strategy: str
    generation_strategy_description: str
    examples: List[str]
    num_results: int
    call_params = OpenAICallParams(model="gpt-4")

    @property
    def few_shot_examples(self) -> str:
        examples_string = ""
        for example in self.examples:
            examples_string = examples_string + example + "\n"
        print(examples_string)
        return examples_string
