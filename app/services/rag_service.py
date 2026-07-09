from http.client import HTTPException
from pathlib import Path

import time
from app.models.schemas import QueryRequest, QueryResponse
from ingestion.pipeline import run_pipeline


def process_query(query: str, file_path: str | None = None):
    if not file_path:
        raise HTTPException(
            status_code=404, detail=f"File path not found : {file_path}"
        )

    # file_path = "data/sample_test.txt"
    path = Path(file_path).resolve()
    if not path:
        raise HTTPException(status_code=404, detail=f"File path not found : {path}")

    print("Resolved Path :: " + str(path))
    print("Exists :: " + str(path.exists()))

    answer = run_pipeline(path, query)
    start = time.perf_counter()

    response = QueryResponse(
        # answer=f"Received Query {query} and file {file_path}",
        # sources=["chunk_ID", "source_filename", "citations"],
        # sources=[file_path or "default"],
        answer=answer,
        sources=[str(path)],
        latency_ms=int(time.perf_counter() - start),
    )
    return response
