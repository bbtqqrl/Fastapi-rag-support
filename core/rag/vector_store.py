from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.document_chunk import DocumentChunk

async def insert_chunks(db: AsyncSession, document_id, chunks: list[str], embeddings: list[list[float]],) -> None:
    assert len(chunks) == len(embeddings)

    objects = [
        DocumentChunk(
            document_id=document_id,
            content=chunk,
            embedding=embedding,
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    db.add_all(objects)
    await db.commit()


async def search_chunks(db: AsyncSession, query_embedding: list[float],limit: int = 14,) -> list[str]:
    stmt = (
        select(DocumentChunk)
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    
    result = await db.execute(stmt)
    rows = result.scalars().all()
    
    return [row.content for row in rows]


