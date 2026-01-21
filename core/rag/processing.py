import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks


async def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts, 
    )
    return [item.embedding for item in response.data]

