from pathlib import Path

from app.models.schemas import QueryRequest, QueryResponse
from ingestion.pipeline import run_pipeline


def process_query(query: str, file_path: str | None = None):
    if not file_path:
        raise ValueError("File Path Not Found")

    # file_path = "data/sample_test.txt"
    path = Path(file_path).resolve()

    print("Resolved Path :: " + str(path))
    print("Exists :: " + str(path.exists()))

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    answer = run_pipeline(path, query)
    response = QueryResponse(
        # answer=f"Received Query {query} and file {file_path}",
        # sources=["chunk_ID", "source_filename", "citations"],
        # sources=[file_path or "default"],
        answer=answer,
        sources=[str(path)],
        latency_ms=0,
    )
    return response
