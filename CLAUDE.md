# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LangChain chatbot application with dual interfaces (CLI + Streamlit web UI) using Ollama as the LLM provider. Uses a modular architecture with `src/` for the core application.

## Code Flow (LangChain + Ollama)

### LangChain Architecture

The application follows LangChain's composition pattern using LCEL (LangChain Expression Language):

```
User Input → ChatPromptTemplate → ChatOllama → StrOutputParser → Response
                    ↑                                      ↓
              chat_history ←─────────────────────── AI Message
```

### Key Components

1. **ChatPromptTemplate**: Composes messages (system + history + user input)
   - `ChatPromptTemplate.from_messages()` creates the template
   - `MessagesPlaceholder` injects conversation history

2. **ChatOllama**: LLM provider connecting to local Ollama instance
   - `model`: Ollama model name (e.g., `minimax-m2.5:cloud`)
   - `temperature`: Controls randomness (0.0-2.0)

3. **StrOutputParser**: Parses LLM output to string

4. **LCEL Chain**: `prompt | llm | StrOutputParser` chains components together

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input (question)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  ChatPromptTemplate                                         │
│  - System prompt (instructions)                            │
│  - MessagesPlaceholder (chat_history)                      │
│  - Human message (user input)                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  ChatOllama (Ollama LLM)                                    │
│  - Sends formatted prompt to local Ollama                  │
│  - Receives AI response                                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  StrOutputParser                                            │
│  - Converts AIMessage to plain string                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Response + Update chat_history                            │
│  - Append HumanMessage(user_input)                         │
│  - Append AIMessage(response)                              │
└─────────────────────────────────────────────────────────────┘
```

## Commands

### Run CLI
```bash
python app.py
```

### Run Streamlit Web UI
```bash
streamlit run streamlit_app.py
```

### Run FastAPI Server
```bash
uvicorn src.main:app --reload
```

### Install dependencies
```bash
uv sync
```

## Architecture

### Root Files
- **`app.py`**: CLI entry point - simple text-based chat interface
- **`streamlit_app.py`**: Streamlit web UI with sidebar settings
- **`chatbot.py`**: Shared chat logic and ChatBot class

### chatbot.py Modules
- `get_available_models()`: Lists available Ollama models via `ollama list`
- `create_llm()`: Factory function for ChatOllama instance
- `create_prompt()`: Factory for ChatPromptTemplate
- `create_chain()`: Composes LCEL chain (prompt | llm | parser)
- `ChatBot` class: Stateful chatbot with conversation management
- `chat()`: Legacy function for backward compatibility

### src/ Directory (Modular Architecture)
- **`src/main.py`**: FastAPI application entry point
- **`src/api/`**: API route handlers and endpoints
- **`src/config/`**: Configuration settings and environment variables
- **`src/core/`**: Core utilities (logging, exceptions, constants)
- **`src/models/`**: Pydantic models, schemas, data structures
- **`src/providers/`**: LLM provider integrations (Ollama, OpenAI)
- **`src/services/`**: Business logic services

## Environment

Create `.env` with:
```env
OLLAMA_MODEL=minimax-m2.5:cloud
TEMPERATURE=0.7
MAX_TURNS=5
SYSTEM_PROMPT=You are a helpful assistant.
```

## Key LangChain Concepts Used

| Concept | Usage in Code |
|---------|---------------|
| LCEL | `prompt \| llm \| StrOutputParser` |
| Messages | `HumanMessage`, `AIMessage` |
| Prompt Template | `ChatPromptTemplate.from_messages()` |
| Output Parser | `StrOutputParser()` |
| Chain | `create_chain()` function |
| Ollama Integration | `ChatOllama` from `langchain_ollama` |
