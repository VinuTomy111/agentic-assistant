import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
NOTES_DIR = os.path.join(MEMORY_DIR, "notes")

# Ensure required directories exist
os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(NOTES_DIR, exist_ok=True)

if not GROQ_API_KEY:
    import logging
    logging.warning("GROQ_API_KEY is not set. Please update your .env file.")
