from embedder.image_embeddings import generate_face_embedding
from pinecone import Index

async def query_pinecone(image_path: str, index: Index, top_k: int = 1):
    """Queries Pinecone with an Image"""

    query_embedding = await generate_face_embedding(image_path)
    result = index.query(vector=query_embedding, top_k=top_k,include_metadata=True)

    return result["matches"]
