from duckduckgo_search import DDGS
import logging

def search_web(query: str, max_results: int = 3) -> str:
    """
    Perform a web search using DuckDuckGo.
    """
    logging.info(f"Using tool: search_web with query: '{query}'")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "No results found."
            
        formatted_results = []
        for i, res in enumerate(results):
            title = res.get('title', 'No Title')
            body = res.get('body', 'No Description')
            href = res.get('href', 'No URL')
            formatted_results.append(f"[{i+1}] {title}\nURL: {href}\nSnippet: {body}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        error_msg = f"Error during web search: {str(e)}"
        logging.error(error_msg)
        return error_msg
