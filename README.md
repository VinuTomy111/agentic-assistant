# Agentic Assistant

A Python-based personal AI assistant that plans tasks, executes tool calls, and responds through either a terminal chat UI or a Streamlit web app.

## Features

- Planner/Executor agent pattern
- Tool-enabled actions:
  - `search_web` (DuckDuckGo search)
  - `calculate` (safe arithmetic evaluator)
  - `save_note` and `retrieve_note` (markdown-based notes)
- Short-term conversational memory
- Long-term JSON-backed memory retrieval
- Two interfaces:
  - CLI (`main.py`)
  - Web app (`app.py`)

## Requirements

- Python 3.9+
- A valid Groq API key

## Installation

```bash
python -m venv .venv
```

Activate your virtual environment:

- Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
LOG_LEVEL=INFO
```

## Run the Assistant

### CLI Mode

```bash
python main.py
```

Type `exit`, `quit`, or `q` to stop.

### Streamlit Mode

```bash
streamlit run app.py
```
