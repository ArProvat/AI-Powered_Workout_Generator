from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()   


# Initialize the Groq LLM
llm = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=0.3,
    reasoning_format="parsed",
    max_retries=2,
)