from langchain_groq import ChatGroq

# Initialize the Groq LLM
LLMs = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=0.3,
    reasoning_format="parsed",
    max_retries=2,
)