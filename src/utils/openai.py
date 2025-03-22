import logging
from langchain_openai import OpenAI

def initialize_openai(user_api_key: str) -> OpenAI|None:
    """Initializes and return a Pinecone client object"""

    try:
        openai = OpenAI(api_key=user_api_key)
        return openai
    except Exception as e:
        logging.warning(f"Error when initializing Pinecone: {e}")
        return None