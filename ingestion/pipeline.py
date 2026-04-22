"""
Pipeline :: orchestrator
 Orchestrates the flow of data through the system.
 Takes a log file as input.
 Outputs embedded vectors.
 Uses components from the ingestion module.
 Uses components from the retrieval module.
"""

from ingestion.chunk_sessions import ChunkSession
from ingestion.embedding_prep import EmbeddingPrepare
from ingestion.normalizer import Normalizer
from ingestion.parser import parse_log_segment, read_logs
from ingestion.sessionizer import Sessionizer
from retrieval.embedder import Embedder


def run_pipeline(log_file):
    # Step 1: Generators
    log_gen = read_logs(log_file)
    parsed_gen = parse_log_segment(log_gen)

    # Step 2: Components
    normalizer = Normalizer()
    sessionizer = Sessionizer()
    chunker = ChunkSession()
    embedding_prepper = EmbeddingPrepare()
    embed_to_vector = Embedder()

    # Step 3: Flow
    for msg in parsed_gen:
        normalized_msg = normalizer.normalize(msg)
        sessionizer.process(normalized_msg)

    # Step 4: Get result
    session_result = sessionizer.get_sessions()

    # Step 5: Create Chunks
    chunk_result = chunker.chunk_sessions_func(session_result)

    # Step 6: Prepare Embeddings
    embed_prep_result = embedding_prepper.embed_chunks(chunk_result)

    # Step 7: Embed to Vector DB
    result = embed_to_vector.embed_text(embed_prep_result)
    return result
