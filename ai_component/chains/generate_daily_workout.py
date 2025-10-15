from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from ai_component.prompts.prompts import system_prompt , daily_workout_prompt
from ai_component.LLMs.Groq_llm import llm
from ai_component.schemas.response_sehema import format_instructions ,parser
from ai_component.short_term_memory.redis_short_term_memory import get_redis_memory as get_redis_history 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages.utils import trim_messages
import json

def get_daily_workout_chain(user_input:dict,session_id:str):
    """Create a chain to generate a daily workout plan."""
    try:
        # 1. Define the Prompt Template (Unchanged)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"), 
            ("human", '{input}')
        ])

        # 2. Define the History Trimmer (Unchanged)
        trimmer = trim_messages(
            max_tokens=14, 
            token_counter=len, # Count by message (not tokens)
            strategy="last",   # Keep the most recent messages
        )
        

        history_trimmer_chain = RunnablePassthrough.assign(
            history=lambda x: trimmer.invoke(x["history"])
        )

        
        chain = history_trimmer_chain | prompt | llm | StrOutputParser()

        # 5. Wrap the chain with RunnableWithMessageHistory (Unchanged)
        workout_chain_with_history = RunnableWithMessageHistory(
            chain,
            get_session_history=get_redis_history,
            input_messages_key="input",
            history_messages_key="history"
        )

        # 6. Invoke the WRAPPED chain (Unchanged)
        content = workout_chain_with_history.invoke(
            {"input": daily_workout_prompt.format(**user_input), 'format_instructions': format_instructions},
            config={"configurable": {"session_id": session_id}}
        )

        print(f"Raw LLM Output: {content}")
        
        try:
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            workout_plan = content.strip()
            return workout_plan
        except:
            pass
            
    except Exception as e:
        print(f"Error in get_daily_workout_chain: {e}")
        return str(e)