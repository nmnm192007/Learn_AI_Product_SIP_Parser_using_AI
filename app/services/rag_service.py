from app.models.schemas import QueryRequest, QueryResponse


def process_query(query: str):
    response = QueryResponse(
        answer="This is a dummy answer",
        sources=["chunk_ID", "source_filename", "citations"],
        latency_ms=100,
    )
    return response
