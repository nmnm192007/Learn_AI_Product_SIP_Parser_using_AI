from typing import Dict, List


class EmbeddingPrepare:
    """
    Prepares chunks of session data for embedding.
    This class is responsible for formatting the session chunks
    into a text format suitable for embedding.
    """

    def embed_chunks(self, chunks: Dict[str, List[Dict[str, str]]]):
        chunks_embed_prep = []

        for call_id, chunk_list in chunks.items():
            for chunk in chunk_list:
                chunk_to_text = self._build_chunk_text(chunk)
                chunks_embed_prep.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "chunk_text": chunk_to_text,
                        "metadata": {
                            "call_id": call_id,
                            "type": chunk["type"],
                            "error_code": chunk["error_code"],
                            "session_start_time": chunk["session_start_time"],
                            "session_duration_sec": chunk["session_duration_sec"],
                            "error_text": chunk["error_text"],
                        },
                    }
                )

        # print(chunks_embed_prep)

        return chunks_embed_prep

    def _build_chunk_text(self, chunk: Dict[str, str]):
        messages = " ".join(
            msg.replace("OTHER::", "") for msg in chunk.get("messages", [])
        )
        error_text = chunk.get("error_text") or "No Error Text"
        error_code = chunk.get("error_code") or "No Error Code"

        return (
            f"Type: {chunk['type']} | "
            f"Messages: {messages} | "
            f"Error: {error_text} | "
            f"Code: {error_code} | "
            f"Duration: {chunk['session_duration_sec']}"
        )
