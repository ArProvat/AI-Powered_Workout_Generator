from langchain_community.chat_message_histories import UpstashRedisChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

# Function to get Redis-based chat message history
def get_redis_memory(session_id: str) -> UpstashRedisChatMessageHistory:
    redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
    redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    return UpstashRedisChatMessageHistory(
        session_id=session_id,
        redis_url=redis_url,
        redis_token=redis_token,
    )