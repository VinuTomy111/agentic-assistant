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

## Project Structure

- `main.py` - Terminal chat assistant with Rich UI
- `app.py` - Streamlit chat interface
- `agents/` - Planner and executor agents
- `tools/` - Search, calculator, and note tools
- `memory/` - Short-term and long-term memory modules
- `storage/` - Runtime memory and notes directory (auto-created)
- `config.py` - Environment/config loading

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

## How It Works

1. User query is added to short-term memory.
2. Planner agent creates a JSON plan with tool steps.
3. Executor agent runs matching tools from `tools/`.
4. Synthesizer model generates the final user-facing response.

## Notes and Memory Storage

- Long-term memory file: `storage/long_term.json`
- Saved notes: `storage/notes/*.md`

These directories/files are created automatically when the app starts.

## Troubleshooting

- **`GROQ_API_KEY` missing**: set it in `.env`.
- **No response generated**: check your API key validity and internet access.
- **Streamlit not found**: reinstall dependencies with `pip install -r requirements.txt`.
