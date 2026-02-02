from .parsing import parse_file
from .processing import chunk_text, embed_texts, rerank_chunks, rewrite_query,chunk_faq
from .vector_store import insert_chunks, search_chunks

async def ingest_file(db, filename: str, file_bytes: bytes, document_id,):
    text = parse_file(filename, file_bytes)
    chunks = chunk_faq(text) 
    embeddings = await embed_texts(chunks)

    await insert_chunks(db, document_id, chunks, embeddings)


async def retrieve_context(db, query: str, limit: int = 3) -> list[str]:
    query_embedding = (await embed_texts([query]))[0]
    context_chunks = await search_chunks(db, query_embedding, limit=limit)
    return context_chunks