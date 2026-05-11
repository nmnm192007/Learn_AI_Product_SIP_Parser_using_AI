from app.models.schemas import QueryRequest, QueryResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to AI based SIP call flow analyser"}


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI SIP Logs Analyser",
        "version": "2.0",
    }


@router.post("/query", response_model=QueryResponse)
def query_check(request: QueryRequest):
    response = QueryResponse(
        answer="This is a dummy answer",
        sources=["chunk_ID", "source_filename", "citations"],
        latency_ms=100,
    )
    return response
