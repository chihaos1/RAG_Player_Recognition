import os
import shutil
from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
from querier.image_query import query_pinecone
from utils.pinecone import initialize_pinecone

router = APIRouter( 
    prefix="/query",
    tags=["query"]
) 

load_dotenv(find_dotenv())
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "player-images"
UPLOAD_DIR = Path.cwd().parent / "data" / "query"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/image/")
async def upload_query_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"message": "File is not an image"})

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    pinecone = initialize_pinecone(PINECONE_API_KEY)
    index = pinecone.Index(PINECONE_INDEX_NAME)
    response = await query_pinecone(file_location, index)

    return response