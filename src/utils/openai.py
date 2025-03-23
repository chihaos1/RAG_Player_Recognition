import logging
from langchain.chat_models import ChatOpenAI

def initialize_openai(user_api_key: str) -> ChatOpenAI|None:
    """Initializes and return a Pinecone client object"""

    try:
        llm = ChatOpenAI(api_key=user_api_key, model_name="gpt-4o")
        return llm
    except Exception as e:
        logging.warning(f"Error when initializing Pinecone: {e}")
        return None