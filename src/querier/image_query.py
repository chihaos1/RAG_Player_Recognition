import re
from embedder.image_embeddings import generate_face_embedding
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from pinecone import Index

async def query_pinecone(image_path: str, index: Index, top_k: int = 1):
    """Queries Pinecone with an Image"""

    query_embedding = await generate_face_embedding(image_path)
    result = index.query(vector=query_embedding, top_k=top_k,include_metadata=True)
    image_name = result["matches"][0]["metadata"]["image_name"]
    player_name = re.search("(.+)_\d+", image_name).group(1) #Extracts player name from image name metadata

    return player_name

async def query_openai(player_name: str):
    """Queries OpenAI about the provided player
    
    """

    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(content='You are a soccer expert and analyst.'),
        HumanMessagePromptTemplate.from_template(content=
            'Who is {player_name}? Provide his career history and play style. 3 bullet points for each.')
    ])

    chat_template.format_messages(player_name=player_name)
