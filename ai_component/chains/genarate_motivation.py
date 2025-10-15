
from ai_component.prompts.prompts import motivation_system_prompt, motivation_prompt
from langchain.prompts import ChatPromptTemplate
from ai_component.LLMs.Groq_llm import llm
from langchain_core.output_parsers import StrOutputParser

def get_motivation_chain(user_input: dict):
    """Create a chain to generate motivational messages."""
    try:
        prompt = ChatPromptTemplate.from_messages([
        ("system",
            motivation_system_prompt
        ),
        ("human",
            motivation_prompt.format(**user_input)
        ),
    ])
        chain = prompt | llm | StrOutputParser()
        motivational_text = chain.invoke({})
        print(f"Motivational Text: {motivational_text}")
        return motivational_text
    except Exception as e:
       print(f"Error in get_motivation_chain: {e}")
       return str(e)
