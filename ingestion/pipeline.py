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
from llm.llm_client import LLMClient
from llm.prompt_builder import PromptBuilder
from retrieval.embedder import Embedder
from retrieval.qdrant_client import QdrantVectorDB
from retrieval.retriever import Retriever


def run_pipeline(log_file):
    print(":::Pipeline Started:::")
    query_text = (
        "explain which all were the successful calls, also explain when call failed"
    )
    # Step 1: Generators
    log_gen = read_logs(log_file)
    parsed_gen = parse_log_segment(log_gen)

    # Step 2: Components
    normalizer = Normalizer()
    sessionizer = Sessionizer()
    chunker = ChunkSession()
    embedding_prepper = EmbeddingPrepare()
    embed_to_vector = Embedder()
    q_vector_db = QdrantVectorDB()
    retriever_obj = Retriever(q_vector_db)
    prompt_obj = PromptBuilder()
    llm_obj = LLMClient()

    print(":::All Components Loaded:::")

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
    emb_chunks = embed_to_vector.embed_text(embed_prep_result)

    # Step 8: Store in Vector DB
    emb_obj = q_vector_db.store_embeddings(emb_chunks)

    # Step 9: Retrieve from Vector DB
    retrieved_chunks = retriever_obj.start_search(query_text)

    if not retrieved_chunks:
        return "No Relevant data found"

    # Step 10: Build Prompt
    prompt = prompt_obj.build_prompt(query_text, retrieved_chunks)

    # Step 11: LLM Generate
    answer_result = llm_obj.generate_response(prompt)
    return answer_result
