# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LangChain chatbot application with dual interfaces (CLI + Streamlit web UI) using Ollama as the LLM provider. Uses a modular architecture with src/ for the core application.

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
- **`chatbot.py`**: Shared chat logic (to be migrated to src/)

### src/ Directory (Modular Architecture)
- **`src/main.py`**: FastAPI application entry point
- **`src/api/`**: API route handlers and endpoints
- **`src/config/`**: Configuration settings and environment variables
- **`src/core/`**: Core utilities (logging, exceptions, constants)
- **`src/models/`**: Pydantic models, schemas, data structures
- **`src/providers/`**: LLM provider integrations (Ollama, OpenAI)
- **`src/services/`**: Business logic services

## Environment

Create `.env` with `OLLAMA_MODEL=minimax-m2.5:cloud` to override default model.
