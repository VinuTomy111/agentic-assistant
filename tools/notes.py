import os
import glob
import logging
from config import NOTES_DIR

def save_note(title: str, content: str) -> str:
    """
    Save a note to a markdown file.
    """
    logging.info(f"Using tool: save_note with title: '{title}'")
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    safe_title = safe_title.replace(' ', '_').lower()
    
    if not safe_title:
         safe_title = "untitled_note"
         
    filepath = os.path.join(NOTES_DIR, f"{safe_title}.md")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Note successfully saved to {filepath}"
    except Exception as e:
        error_msg = f"Failed to save note: {str(e)}"
        logging.error(error_msg)
        return error_msg

def retrieve_note(query: str) -> str:
    """
    Finds a note matching the query by scanning filenames and content.
    """
    logging.info(f"Using tool: retrieve_note with query: '{query}'")
    query = query.lower()
    notes_files = glob.glob(os.path.join(NOTES_DIR, "*.md"))
    
    if not notes_files:
        return "No notes found in the system."
        
    found_notes = []
    for filepath in notes_files:
        filename = os.path.basename(filepath).lower()
        try:
             with open(filepath, 'r', encoding='utf-8') as f:
                 content = f.read()
             
             if query in filename or query in content.lower():
                 found_notes.append(f"--- Note File: {filename} ---\n{content}\n")
        except Exception as e:
             logging.warning(f"Could not read {filepath}: {str(e)}")
             continue
             
    if found_notes:
         return "\n".join(found_notes)
    else:
         return f"No note matching '{query}' was found."
