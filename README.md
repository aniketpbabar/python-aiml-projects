# Python AI Projects

Small Python projects that show what an AI app looks like inside. Each one is short, runs end to end, and maps to real Python topics you need to learn for AI.

## What's inside

| # | Project | What it does |
|---|---|---|
| 1 | First call | Send a prompt to the model, get a response back. The smallest possible AI app. |
| 2 | Chatbot with memory | A CLI chatbot that remembers the conversation until you type quit. |
| 3 | Structuring messy data | Turn messy customer reviews into clean structured JSON with Pydantic. |
| 4 | Ask your documents | A basic RAG setup using ChromaDB to answer questions about a folder of docs. |
| 5 | Agent with tools | The model decides which tools to call to answer a question. |
| 6 | Specialized model | Classify reviews using a small Hugging Face model that runs locally, no API key needed. |

## Setup

You need Python 3.11 or newer.

1. Clone the repo:
   ```bash
   git clone https://github.com/DataWithBaraa/python-ai-projects.git
   cd python-ai-projects
   ```

2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   On Windows use `.venv\Scripts\activate` instead.

   Then install:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your API key:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and paste your Anthropic key. You can get one at https://console.anthropic.com.

   Project 6 does not need any API key. It downloads a small model the first time you run it.

## Run a project

```bash
python src/01_first_call.py
```

Swap the filename to run any of the others.

## Use OpenAI instead of Anthropic

The default examples use Claude through the Anthropic SDK, but the same code works with OpenAI with small changes:

1. Install the SDK: `pip install openai`
2. Change the import: `from openai import OpenAI`
3. Use the OpenAI client: `client = OpenAI()` and call `client.chat.completions.create(...)`.
4. Put `OPENAI_API_KEY=...` in your `.env` file.

The flow is the same: send messages, get a response back. Pick whatever model fits your use case and budget.

## Files

- `src/` the Python scripts, one per project
- `data/` sample data (messy reviews + a few docs for the RAG example)
- `config.json` model name and file paths
- `.env.example` template for your API key
