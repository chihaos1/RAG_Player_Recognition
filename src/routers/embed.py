
from fastapi import APIRouter
from modules import generate_embeddings, upload_to_pinecone, delete_folders
from starlette import status
from utils.pinecone import PineconeClient

router = APIRouter( 
    prefix="/embed",
    tags=["embed"]
) 

@router.get("/images", status_code=status.HTTP_200_OK)
def embed_player_images() -> None:
    image_embeddings = list()
    client = PineconeClient()
    index = client.initialize_pinecone()
    vector_count = index.describe_index_stats()["total_vector_count"]

    if vector_count:
        index.delete(delete_all=True)

    image_embeddings = generate_embeddings()
    upload_to_pinecone(index, image_embeddings)
    delete_folders() #Deletes player image folders after uploading

    return f"Uploaded {len(image_embeddings)} images to Pinecone and deleted scraped images."
