import logging
from pinecone import Pinecone, ServerlessSpec

#INITIALIZE
def initialize_pinecone(user_api_key: str) -> Pinecone|None:
    """Initializes and return a Pinecone client object"""

    try:
        pinecone = Pinecone(api_key=user_api_key)
        return pinecone
    except Exception as e:
        logging.warning(f"Error when initializing Pinecone: {e}")
        return None

def create_pinecone_index(index_name: str, pinecone: Pinecone) -> None:
    """Creates the Pinecone index for storing player images. Only needs to run once"""
    
    if index_name not in pinecone.list_indexes().names():
        pinecone.create_index(
            name = index_name,
            dimension = 128,
            metric = "cosine",
            spec = ServerlessSpec(
                cloud = "aws",
                region = "us-east-1"
            )
        )
    else:
        print(f"Index {index_name} already exists!")
        return