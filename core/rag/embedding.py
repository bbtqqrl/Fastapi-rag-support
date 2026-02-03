from llm_client import llm_client

async def embed_texts(texts: list[str], model: str) -> list[list[float]]:
    response = await llm_client.embeddings.create(
        model=model,
        input=texts, 
    )
    return [item.embedding for item in response.data]