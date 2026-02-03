import numpy as np
from sentence_transformers import CrossEncoder

async def rerank_chunks(chunks, query, limit: int = 3) -> list[str]:
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    pairs = [(query, chunk) for chunk in chunks]
    scores = model.predict(pairs, show_progress_bar=False)

    ranked = [chunks[i] for i in np.argsort(scores)[::-1]]
    return ranked[0:limit]
