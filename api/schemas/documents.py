from typing import Optional
from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    parser: str = "pdf"
    chunk_strategy: str = "semantic"
    chunk_size: Optional[int] = None
    threshold: Optional[float] = None


class DocumentUploadResponse(BaseModel):
    document_id: int
    filename: str
    status: str
    chunks_count: int
