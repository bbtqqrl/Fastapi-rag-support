from .parsing import parse_file
from .processing import chunk_text, embed_texts
from .vector_store import insert_chunks, search_chunks

async def ingest_file(db, filename: str, file_bytes: bytes, document_id,):
    text = parse_file(filename, file_bytes)
    chunks = chunk_text(text)
    embeddings = await embed_texts(chunks)

    await insert_chunks(db, document_id, chunks, embeddings)


async def retrieve_context(db, query: str, limit: int = 5,) -> list[str]:
    query_embedding = await embed_texts([query])
    result = await search_chunks(db, query_embedding, limit)
    return result