import os
import re
from typing import List
import numpy as np
import json
from openai import AsyncOpenAI
from chonkie import SemanticChunker
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv
from torch import chunk

from .prompting.rewriting_prompt import REWRITING_QUERY_SYSTEM_PROMPT

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def rerank_chunks(chunks, query, limit: int = 3) -> list[str]:
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    pairs = [(query, chunk) for chunk in chunks]
    scores = model.predict(pairs, show_progress_bar=False)

    ranked = [chunks[i] for i in np.argsort(scores)[::-1]]
    return ranked[0:limit]


async def embed_texts(texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=texts, 
    )
    return [item.embedding for item in response.data]
    

async def rewrite_query(query: str, chat_history = None) -> str:
    prompt = REWRITING_QUERY_SYSTEM_PROMPT.format(query=query)
    
    if chat_history:
        prompt += f"\n\nConversation context: {chat_history[-3:]}"  
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100
    )
    try:
        data = json.loads(response.choices[0].message.content.strip())
        if isinstance(data, list):
            print(data)
            return data

        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    return data[key]
    except json.JSONDecodeError:
        pass

    return response

