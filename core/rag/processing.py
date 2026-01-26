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


def chunk_text(text: str) -> list[str]:
    chunker = SemanticChunker(
        embedding_model="minishlab/potion-base-32M",
        threshold=0.7,
        chunk_size=2048,
        skip_window=1  
    )
    chunks = [chunk.text for chunk in chunker.chunk(text)]
    return chunks


def chunk_faq(text: str) -> List[str]:
    section_pattern = re.compile(r"^(\d+)\.\s+(.*)")
    question_pattern = re.compile(r"^(\d+\.\d+)\.\s+(.*)")

    chunks: List[str] = []

    current_section: str | None = None
    current_question: str | None = None
    current_answer_lines: List[str] = []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    print(lines)

    for line in lines:
        # Розділ: "1. Про нас"
        section_match = section_pattern.match(line)
        if section_match and not question_pattern.match(line):
            current_section = section_match.group(2)
            continue


        question_match = question_pattern.match(line)
        if question_match:
            if current_question:
                chunk_parts = []
                if current_section:
                    chunk_parts.append(f"{current_section}.")
                chunk_parts.append(f"{current_question}.")
                chunk_parts.append(" ".join(current_answer_lines))  
                chunks.append(" ".join(chunk_parts))

            current_question = question_match.group(2)
            current_answer_lines = []
            continue

        # Рядок відповіді
        current_answer_lines.append(line)

    # Додаємо останній чанк
    if current_question:
        chunk_parts = []
        if current_section:
            chunk_parts.append(f"{current_section}.")
        chunk_parts.append(f"{current_question}.")
        chunk_parts.append(" ".join(current_answer_lines))  
        chunks.append(" ".join(chunk_parts))

    for chunk in chunks:
        print("---- CHUNK ----")
        print(chunk)
        print("---------------")

    return chunks


async def rerank_chunks(chunks, query, limit: int = 3) -> list[str]:
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    pairs = [(query, chunk) for chunk in chunks]
    scores = model.predict(pairs, show_progress_bar=False)

    print("Reranking scores:", scores)

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