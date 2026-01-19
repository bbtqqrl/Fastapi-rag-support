from pydantic import BaseModel

class AnalyticCreate(BaseModel):
    converstion_id: int

class AnalyticResponse(BaseModel):
    id: int
    total_messages: int
    user_messages: int
    assistant_messages: int
    avg_confidence: float | None
    avg_latency_ms: int | None
    total_tokens: int | None
    resolved: bool
    created_at: str

    class Config:
        from_attributes = True