from .search import search_web
from .calculator import calculate
from .notes import save_note, retrieve_note

AVAILABLE_TOOLS = {
    "search_web": search_web,
    "calculate": calculate,
    "save_note": save_note,
    "retrieve_note": retrieve_note
}

TOOL_DESCRIPTIONS = """
1. search_web(query: str): Performs a web search and returns snippets of information.
2. calculate(expression: str): Evaluates a basic math expression (e.g. "500 * 12"). Returns string result.
3. save_note(title: str, content: str): Saves a text note/idea for long term to disk.
4. retrieve_note(query: str): Retrieves saved notes matching a keyword or query.
"""
