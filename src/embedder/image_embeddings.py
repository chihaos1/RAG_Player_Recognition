import logging
import re
from asyncio import to_thread
from deepface import DeepFace
from os import listdir
from pathlib import Path
from pinecone import Index
from typing import AsyncGenerator, Dict, List

#GET IAMGES
async def _get_all_folders() -> List[str]:
    """Gets the locations of all player folders in the data folder"""

    parent_path = Path(Path.cwd().parent / f"data/images")
    folder_paths = await to_thread(listdir, parent_path)
    return [parent_path / folder_path for folder_path in folder_paths]

async def _get_all_images() -> AsyncGenerator:
    """Gets the locations of all player images in the data folder"""
    
    player_folder_paths = await _get_all_folders()
    for folder in player_folder_paths:
        image_files = await to_thread(listdir, folder)
        for image in image_files:
            image_id = re.search("(\d+)", image).group(1)
            image_name = Path(image).stem
            logging.info(f"Sending to Embed: {folder / image}")
            yield image_id, folder / image, image_name

#EMBEDDING
async def generate_face_embedding(image_path: str):
    """Generates a FaceNet embedding for an image"""
    try:
        embedding = DeepFace.represent(image_path, model_name="Facenet", enforce_detection=False)
        return embedding[0]["embedding"]
    except Exception as e:
        print(f"Error in face embedding generation: {e}")
        return None

async def embed_player_images() -> List[Dict]:
    """Embeds player images"""
    
    face_embeddings = list()

    async for image_id, image_path, image_name in _get_all_images():
        face_embedding = await generate_face_embedding(image_path)
        face_embeddings.append({
            "id": image_id,
            "values": face_embedding,
            "metadata": {"image_name":image_name}
        })
    logging.info(f"Created {len(face_embeddings)} embeddings.")
    return face_embeddings

#UPLOAD
async def upload_to_pinecone(image_embeddings: List[Dict], index: Index) -> None:
    """Uploads player image embeddings to Pinecone index"""

    if image_embeddings:
        index.upsert(image_embeddings)
        logging.info(f"Uploaded {len(image_embeddings)} images to Pinecone.")
    else:
        logging.warning("No valid images found.")

