# LangChain ChatBot

A modular LangChain chatbot application with dual interfaces (CLI + Streamlit web UI) powered by Ollama as the LLM provider.

## Features

- **Dual Interfaces**: CLI and Streamlit web UI
- **Configurable Settings**: Model selection, temperature, max turns, system prompt
- **Chat History**: Persistent conversation context with turn tracking
- **Context Management**: Warning when approaching conversation limits
- **Modular Architecture**: Clean separation with `src/` directory

## Quick Start

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running

### Installation

```bash
# Install dependencies
uv sync
```

### Configuration

Create a `.env` file to customize defaults:

```env
OLLAMA_MODEL=minimax-m2.5:cloud
TEMPERATURE=0.7
MAX_TURNS=5
SYSTEM_PROMPT=You are a helpful assistant.
```

### Running the Application

**CLI Interface:**
```bash
python app.py
```

**Streamlit Web UI:**
```bash
streamlit run streamlit_app.py
```

**FastAPI Server:**
```bash
uvicorn src.main:app --reload
```

## Project Structure

```
langchain-chatbot/
├── app.py                 # CLI entry point
├── streamlit_app.py       # Streamlit web UI
├── chatbot.py             # Shared chat logic
├── src/
│   ├── main.py            # FastAPI application
│   ├── api/               # API route handlers
│   ├── config/            # Configuration settings
│   ├── core/              # Core utilities
│   ├── models/            # Pydantic models
│   ├── providers/         # LLM provider integrations
│   └── services/          # Business logic services
├── pyproject.toml         # Project dependencies
└── README.md
```

## Usage

### CLI Commands
- Type your message and press Enter to chat
- Type `clear` to reset conversation history
- Type `quit` to exit

### Streamlit Interface
- Select model from dropdown
- Adjust temperature (0.0-2.0)
- Set max conversation turns
- Customize system prompt
- Click "Apply Settings" to save changes
- Click "Clear Chat" to start fresh

## Dependencies

- `fastapi` - FastAPI web framework
- `langchain-ollama` - Ollama LLM integration
- `streamlit` - Web UI framework
- `python-dotenv` - Environment variable loading
- `tiktoken` - Tokenization

## License

MIT
