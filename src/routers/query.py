import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from modules import query_pinecone, query_openai
from pathlib import Path
from starlette import status
from utils.pinecone import PineconeClient

router = APIRouter( 
    prefix="/query",
    tags=["query"]
) 

UPLOAD_DIR = Path.cwd().parent / "data" / "query"

@router.post("/image", status_code=status.HTTP_201_CREATED)
async def upload_query_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"message": "File is not an image"})

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    client = PineconeClient()
    index = client.initialize_pinecone()
    player_name = query_pinecone(file_location, index)
    player_summary = query_openai(player_name)

    return player_name, player_summary