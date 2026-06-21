from typing import List

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    file_path: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    latency_ms: int
