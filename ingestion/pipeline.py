"""
Pipeline :: orchestrator
"""

from ingestion.normalizer import Normalizer
from ingestion.parser import read_logs, parse_log_segment
from ingestion.sessionizer import Sessionizer


def run_pipeline(log_file):
    # Step 1: Generators
    log_gen = read_logs(log_file)
    parsed_gen = parse_log_segment(log_gen)

    # Step 2: Components
    normalizer = Normalizer()
    sessionizer = Sessionizer()

    # Step 3: Flow
    for msg in parsed_gen:
        normalized_msg = normalizer.normalize(msg)
        sessionizer.process(normalized_msg)

    # Step 4: Get result
    result = sessionizer.get_sessions()

    return result
