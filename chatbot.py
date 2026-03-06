import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "minimax-m2.5:cloud")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_MAX_TURNS = int(os.getenv("MAX_TURNS", "5"))
DEFAULT_SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant that provides concise and accurate answers.")


def get_available_models():
    """Get list of available Ollama models."""
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        models = []
        for line in result.stdout.strip().split("\n")[1:]:  # Skip header
            if line.strip():
                name = line.split()[0]
                models.append(name)
        return models if models else [DEFAULT_MODEL]
    except Exception:
        return [DEFAULT_MODEL]


def create_llm(model: str, temperature: float):
    """Create a new LLM instance with given parameters."""
    return ChatOllama(model=model, temperature=temperature)  # noqa: F821


def create_prompt(system_prompt: str):
    """Create a new prompt template with given system prompt."""
    return ChatPromptTemplate.from_messages([  # noqa: F821
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),  # noqa: F821
        ("human", "{input}")
    ])


def create_chain(llm, prompt):
    """Create a processing chain."""
    return prompt | llm | StrOutputParser()  # noqa: F821


class ChatBot:
    """ChatBot class with configurable settings."""

    def __init__(self, model: str = None, temperature: float = None,
                 max_turns: int = None, system_prompt: str = None):
        self.model = model or DEFAULT_MODEL
        self.temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
        self.max_turns = max_turns or DEFAULT_MAX_TURNS
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.chat_history = []
        self._update_chain()

    def _update_chain(self):
        """Update the LLM and chain based on current settings."""
        self.llm = create_llm(self.model, self.temperature)
        self.prompt = create_prompt(self.system_prompt)
        self.chain = create_chain(self.llm, self.prompt)

    def update_settings(self, model: str = None, temperature: float = None,
                       max_turns: int = None, system_prompt: str = None):
        """Update chatbot settings."""
        if model is not None:
            self.model = model
        if temperature is not None:
            self.temperature = temperature
        if max_turns is not None:
            self.max_turns = max_turns
        if system_prompt is not None:
            self.system_prompt = system_prompt
        self._update_chain()

    def reset_history(self):
        """Clear chat history."""
        self.chat_history = []

    def chat(self, question: str):
        """Process a question and update chat history.

        Args:
            question: The user's input

        Returns:
            Response string, or warning message if context is full
        """
        current_turns = len(self.chat_history) // 2

        if current_turns >= self.max_turns:
            return (
                "Context window is full. "
                "The AI may not follow your previous thread properly. "
                "Please clear the chat for a new conversation."
            ), self.chat_history

        response = self.chain.invoke({
            "input": question,
            "chat_history": self.chat_history
        })

        self.chat_history.append(HumanMessage(content=question))  # noqa: F821
        self.chat_history.append(AIMessage(content=response))  # noqa: F821

        remaining = self.max_turns - (current_turns + 1)
        warning = ""
        if remaining <= 2:
            warning = f"\n{remaining} turn(s) left."

        return response + warning, self.chat_history


# Legacy functions for backward compatibility
def create_chat_history():
    """Create a new chat history list."""
    return []


def chat(question, chat_history, max_turns=DEFAULT_MAX_TURNS):
    """Legacy chat function."""
    current_turns = len(chat_history) // 2

    if current_turns >= max_turns:
        return (
            "Context window is full. "
            "The AI may not follow your previous thread properly. "
            "Please type 'clear' for a new chat."
        ), chat_history

    llm = ChatOllama(model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE)
    prompt = ChatPromptTemplate.from_messages([
        ("system", DEFAULT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({
        "input": question,
        "chat_history": chat_history
    })

    chat_history.append(HumanMessage(content=question))  # noqa: F821
    chat_history.append(AIMessage(content=response))  # noqa: F821

    remaining = max_turns - (current_turns + 1)
    warning = ""
    if remaining <= 2:
        warning = f"\n{remaining} turn(s) left."

    return response + warning, chat_history


MAX_TURNS = DEFAULT_MAX_TURNS
