
from ai_component.prompts.prompts import system_prompt, motivation_prompt
from langchain.prompts import ChatPromptTemplate
from ai_component.LLMs.Groq_llm import llm
from langchain_core.output_parsers import StrOutputParser

def get_motivation_chain(user_input: dict):
    """Create a chain to generate motivational messages."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", motivation_prompt.format(user_inputs=user_input))
    ])

    chain = prompt | llm | StrOutputParser()
    return chain.invoke(user_input)
