from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOpenAI(
    model_name="mistral",
    openai_api_base="http://localhost:11434/v1",
    openai_api_key="ollama"  # doesn't matter for Ollama
)


system_prompt=(
    "You are an assistant for question-answering tasks."
    "Use the following pieces of retrieved context to answer the question."
    "If you don't know the answer, say that you don't know."
    "Use five sentences maximum and keep the answer concise."
    "Don't answer outside the retrieved context."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","{input}")
    ]
)


