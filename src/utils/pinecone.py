import os
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone

load_dotenv(find_dotenv())

@dataclass
class PineconeClient:
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME")

    def initialize_pinecone(self: str) -> Pinecone|None:
        """Initializes and return a Pinecone client object"""
        try:
            pinecone = Pinecone(api_key=self.PINECONE_API_KEY)
            return self.access_pinecone_index(pinecone)
        except Exception as e:
            return None
        
    def access_pinecone_index(self, pinecone: Pinecone) -> None:
        """Accesses the Pinecone index"""
        return pinecone.Index(self.PINECONE_INDEX_NAME)   


# def create_pinecone_index(index_name: str, pinecone: Pinecone) -> None:
#     """Creates the Pinecone index for storing player images. Only needs to run once"""
    
#     if index_name not in pinecone.list_indexes().names():
#         pinecone.create_index(
#             name = index_name,
#             dimension = 128,
#             metric = "cosine",
#             spec = ServerlessSpec(
#                 cloud = "aws",
#                 region = "us-east-1"
#             )
#         )
#     else:
#         print(f"Index {index_name} already exists!")
#         return