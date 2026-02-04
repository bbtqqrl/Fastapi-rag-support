from .llm_client import client

async def embed_texts(texts: list[str], model: str) -> list[list[float]]:
    response = await client.embeddings.create(
        model=model,
        input=texts, 
    )
    return [item.embedding for item in response.data]