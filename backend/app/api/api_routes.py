from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import process_query
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
def query_fn(request: QueryRequest):
    result = process_query(request.query, request.file_path)
    return result
