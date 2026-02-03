from .parsing import create_parser
from .rewriting_query import rewrite_query
from .reranking import rerank_chunks   
from .embedding import embed_texts
from .chunk_strategy import create_chunker
from .vector_store import insert_chunks, search_chunks

async def ingest_file(
        db, 
        file_bytes: bytes,  
        document_id: int, 
        parser: str, 
        chunk_strategy: str, 
        embedding_model: str = "text-embedding-3-small"
    ) -> None:
    
    parse_file = create_parser(parser)
    text = parse_file.parse(file_bytes)

    chunk_text = create_chunker(chunk_strategy)
    chunks = chunk_text.chunk(text) 

    embeddings = await embed_texts(chunks, embedding_model)

    await insert_chunks(db, document_id, chunks, embeddings)


async def retrieve_context(
        db, 
        query: str, 
        limit: int = 3, 
        use_rerank: bool = False, 
        use_rewrite: bool = False, 
        embedding_model: str = "text-embedding-3-small"
    ) -> list[str]:

    search_limit = limit * 3 if use_rerank else limit

    if use_rewrite:
        query = await rewrite_query(query)

    query_embedding = (await embed_texts([query], embedding_model))[0]
    context_chunks = await search_chunks(db, query_embedding, search_limit)

    if use_rerank:
        context_chunks = await rerank_chunks(context_chunks, query, limit)

    return context_chunks