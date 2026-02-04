from typing import Optional, List
from pydantic import BaseModel


class RAGMessageRequest(BaseModel):
    content: str
    top_k: int = 5
    rewrite_query: bool = False
    rerank: bool = False
    return_chunks: bool = False


class RAGMessageResponse(BaseModel):
    answer: str
    rewritten_query: Optional[str] = None
    used_chunks: Optional[List[str]] = None
    processing_time_ms: float