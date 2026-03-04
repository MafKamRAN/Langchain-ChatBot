from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7,
)

response = llm.invoke("What is RAG?")
print(response.content)

