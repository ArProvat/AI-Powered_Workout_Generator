from langchain_community.chat_message_histories import UpstashRedisChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()


def get_redis_memory(session_id: str) -> UpstashRedisChatMessageHistory:
    redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
    redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    print(f"Redis URL: {redis_url}, Token: {redis_token}, Session ID: {session_id}")
    return UpstashRedisChatMessageHistory(
        session_id=session_id,
        url=redis_url,
        token=redis_token,
    )


