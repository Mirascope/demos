from mirascope import tags
from mirascope.openai import OpenAICall, OpenAICallParams

prev_revision_id = None
revision_id = "0001"


@tags(["version:0001"])
class QueryAnswerPrompt(OpenAICall):
    """Generates code samples for a specific library based upon a given query."""

    prompt_template = """
    SYSTEM:
    You are an expert Python Programmer. You have incredible skills in data science, particularly with the {library_focus} library.
    Users will have queries for you to help them with specific tasks they need. Respond with just code that is succinct, but works perfectly. No talking, just code.
    
    USER:
    {query}
    """

    library_focus: str
    query: str
    base_url = "https://api.groq.com/openai/v1"
    call_params = OpenAICallParams(model="mixtral-8x7b-32768")
