import clip
import logging
import re
from asyncio import to_thread
from os import listdir
from pathlib import Path
from PIL import Image
from pinecone import Index
from torch import cuda, nn, no_grad, Tensor 
from typing import AsyncGenerator, Callable, Dict, List

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
type Preprocessor = Callable[[Image.Image], Tensor]

async def _generate_embedding(image_path:str, device:str, 
                             model:nn.Module, preprocess:Preprocessor):
    """Generates the embeddings to turn raw image data into vectors"""

    try:
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
        with no_grad():
            embedding = model.encode_image(image)
            normalized_embedding = embedding / embedding.norm(dim=-1, keepdim=True)
            return normalized_embedding.cpu().numpy().flatten()
    except Exception as e:
        logging.warning(f"Error processing {image_path}: {e}")
        return None

async def embed_player_images(index: str) -> List[Dict]:
    """Embeds player images"""
    
    image_embeddings = list()
    device = "cuda" if cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    async for image_id, image_path, image_name in _get_all_images():
        image_embedding = await _generate_embedding(image_path,device,model,preprocess)
        image_embeddings.append({
            "id": image_id,
            "values": image_embedding.tolist(),
            "metadata": {"image_name":image_name}
        })
    logging.info(f"Created {len(image_embeddings)} embeddings.")

    return image_embeddings

#UPLOAD
async def upload_to_pinecone(image_embeddings: List[Dict], index: Index) -> None:
    """Uploads player image embeddings to Pinecone index"""

    if image_embeddings:
        index.upsert(image_embeddings)
        logging.info(f"Uploaded {len(image_embeddings)} images to Pinecone.")
    else:
        logging.warning("No valid images found.")

