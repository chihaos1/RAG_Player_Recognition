import logging
import os
import re
import shutil
from asyncio import to_thread
from deepface import DeepFace
from pathlib import Path
from pinecone import Index
from typing import Dict, Generator, List

#GET IAMGES
def get_all_folders() -> List[str]:
    """Gets the locations of all player folders in the data folder (helper function)"""

    parent_path = Path(Path.cwd().parent / f"data/images")
    return [parent_path / folder_path for folder_path in os.listdir(parent_path)]

def get_all_images() -> Generator:
    """Gets the locations of all player images in the data folder"""
    
    player_folder_paths = get_all_folders()
    for folder in player_folder_paths:
        for image in os.listdir(folder):
            image_id = re.search("(\d+)", image).group(1)
            image_name = Path(image).stem
            logging.info(f"Sending to Embed: {folder / image}")
            yield image_id, folder / image, image_name

#EMBEDDING
def generate_embedding(image_path: str) -> List[float]:
    """Generates a FaceNet embedding for an image (helper function)"""
    try:
        embedding = DeepFace.represent(image_path, model_name="Facenet", enforce_detection=False)
        return embedding[0]["embedding"]
    except Exception as e:
        print(f"Error in face embedding generation: {e}")
        return None

def generate_embeddings() -> List[Dict]:
    """Embeds player images"""
    
    image_embeddings = list()

    for image_id, image_path, image_name in get_all_images():
        image_embedding = generate_embedding(image_path)
        image_embeddings.append({
            "id": image_id,
            "values": image_embedding,
            "metadata": {"image_name":image_name}
        })
    logging.info(f"Created {len(image_embeddings)} embeddings.")
    return image_embeddings

#UPLOAD
def upload_to_pinecone(index: Index, image_embeddings: List[Dict]) -> None:
    """Uploads player image embeddings to Pinecone index"""

    if image_embeddings:
        index.upsert(image_embeddings)
        logging.info(f"Uploaded {len(image_embeddings)} images to Pinecone.")
    else:
        logging.warning("No valid images found.")

def delete_folders() -> None:
    """Deletes all the subfolders in data/images after embedding is completed"""

    parent_path = Path(Path.cwd().parent / f"data/images")
    for subfolder in os.listdir(parent_path):
        subfolder_path = os.path.join(parent_path,subfolder)
        if os.path.isdir(subfolder_path):
            shutil.rmtree(subfolder_path)