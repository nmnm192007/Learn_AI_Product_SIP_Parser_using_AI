"""
Pipeline :: orchestrator
"""

from ingestion.chunk_sessions import ChunkSession
from ingestion.normalizer import Normalizer
from ingestion.parser import parse_log_segment, read_logs
from ingestion.sessionizer import Sessionizer


def run_pipeline(log_file):
    # Step 1: Generators
    log_gen = read_logs(log_file)
    parsed_gen = parse_log_segment(log_gen)

    # Step 2: Components
    normalizer = Normalizer()
    sessionizer = Sessionizer()
    chunker = ChunkSession()

    # Step 3: Flow
    for msg in parsed_gen:
        normalized_msg = normalizer.normalize(msg)
        sessionizer.process(normalized_msg)

    # Step 4: Get result
    result = sessionizer.get_sessions()

    # Step 5: Create Chunks
    result = chunker.chunk_sessions_func(result)

    # print(result)
    return result
