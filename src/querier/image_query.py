import logging
import openai
import re
from embedder.image_embeddings import generate_face_embedding
from pinecone import Index

async def query_pinecone(image_path: str, index: Index):
    """Queries Pinecone with an Image"""

    query_embedding = await generate_face_embedding(image_path)
    result = index.query(vector=query_embedding, top_k=1, include_metadata=True)

    if result["matches"][0]["score"] < 50:
        return "No compatible result in the database"
    else:
        image_name = result["matches"][0]["metadata"]["image_name"]
        player_name = re.search("(.+)_\d+", image_name).group(1) #Extracts player name from image name metadata
        logging.info(f"The player from the image is {player_name}")
        return player_name

async def query_openai(player_name: str):
    """Queries OpenAI about the provided player"""
    
    system_prompt = "You are a soccer expert and analyst."
    user_prompt = f"Who is {player_name}? Provide his career history and play style. 3 bullet points for each."
    response = openai.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7, 
    )
    logging.info(f"The is the career and playstyle of {player_name}: {response.choices[0].message.content}")

    return response.choices[0].message.content
