from .parsing import parse_file
from .processing import chunk_text, embed_texts, rerank_chunks, rewrite_query,chunk_faq
from .vector_store import insert_chunks, search_chunks

async def ingest_file(db, filename: str, file_bytes: bytes, document_id,):
    text = parse_file(filename, file_bytes)
    chunks = chunk_faq(text) 
    embeddings = await embed_texts(chunks)

    await insert_chunks(db, document_id, chunks, embeddings)


async def retrieve_context(db, query: str, limit: int = 3) -> list[str]:
    # 1. Генеруємо варіанти запитів
    query_variants = await rewrite_query(query)
    
    # 2. Пошук для кожного варіанту
    all_results = []
    embedding = await embed_texts(query_variants)
    for embedded_query in embedding:
        chunks = await search_chunks(db, embedded_query, limit=8)
        all_results.append(chunks)
    
    # 3. Рахуємо скільки раз кожен чанк зустрічається
    chunk_counts = {}
    for chunks in all_results:
        for chunk in chunks:
            chunk_counts[chunk] = chunk_counts.get(chunk, 0) + 1
    
    # 4. ВИБИРАЄМО СТРАТЕГІЮ:
    print(chunk_counts)
    # А) Чанки, що зустрічаються в ≥2 варіантах
    popular_chunks = [chunk for chunk, count in chunk_counts.items() if count >= 2]
    
    if popular_chunks:
        # ✅ Стратегія 1: просто повертаємо популярні чанки
        # Сортуємо за кількістю входжень (від більшого до меншого)
        popular_chunks_sorted = sorted(
            popular_chunks, 
            key=lambda x: chunk_counts[x], 
            reverse=True
        )
        
        print(f"🎯 Знайдено {len(popular_chunks)} популярних чанків (≥2 варіанти)")
        print(f"🎯 Повертаємо топ-{limit} за популярністю")
        
        return popular_chunks_sorted[:limit]
    
    else:
        # ❌ Стратегія 2: немає популярних чанків → юзаємо реранкер
        print("⚠️  Популярних чанків не знайдено, використовуємо реранкер")
        
        # Збираємо всі унікальні чанки
        all_unique_chunks = list(chunk_counts.keys())
        
        # Реранкінг
        reranked = await rerank_chunks(all_unique_chunks, ' '.join(query_variants))
        
        return reranked[:limit]