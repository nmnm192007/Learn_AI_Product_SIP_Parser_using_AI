from app.models.schemas import QueryRequest, QueryResponse


def process_query(query: str, file_path: str | None = None):
    response = QueryResponse(
        answer=f"Received Query {query} and file {file_path}",
        # sources=["chunk_ID", "source_filename", "citations"],
        sources=[file_path or "default"],
        latency_ms=100,
    )
    return response
