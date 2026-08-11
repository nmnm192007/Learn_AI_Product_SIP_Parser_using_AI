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
                chunk_to_text_enriched = self._build_chunk_text_enriched(chunk)
                call_status = self._derive_call_status(chunk)
                chunks_embed_prep.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "chunk_text": chunk_to_text,
                        "chunk_text_enriched": chunk_to_text_enriched,
                        "metadata": {
                            "call_id": call_id,
                            "type": chunk["type"],
                            "call_status": call_status,
                            "error_code": chunk["error_code"],
                            "session_start_time": chunk["session_start_time"],
                            "session_duration_sec": chunk["session_duration_sec"],
                            "error_text": chunk["error_text"],
                        },
                    }
                )

        print("chunks_embed_prep : " + str(chunks_embed_prep))

        return chunks_embed_prep

    """
        Creates a chunk text that is suitable for embedding.
        This helper function creates a chunk text that is suitable for embedding.
        It formats the chunk information into a string with key-value pairs.
    
        Args:
            chunk (Dict[str, str]): A dictionary containing chunk information.
    
        Returns:
            str: A formatted string suitable for embedding.
    
    """

    # Helper function
    # Creates chunk text that is suitable for embedding.
    def _build_chunk_text(self, chunk: Dict[str, str]):
        messages = " ".join(
            msg.replace("OTHER::", "") for msg in chunk.get("messages", [])
        )
        error_code = chunk.get("error_code") or "No Error Code"
        error_text = chunk.get("error_text") or "No Error Text"

        call_status = self._derive_call_status(chunk)
        return (
            f"Type: {chunk['type']} | "
            f"Messages: {messages} | "
            f"Call Status: {call_status} | "
            f"Error: {error_text} | "
            f"Code: {error_code} | "
            f"Duration: {chunk['session_duration_sec']}"
        )

    """
        Derives the call status based on the error code and error text.
        Args:
            chunk (Dict[str, str]): A dictionary containing chunk information.

        Returns:
            str: The call status, either "SUCCESS" or "FAILURE".
    """

    def _derive_call_status(self, chunk: Dict[str, str]) -> str:
        error_code = chunk.get("error_code")
        error_text = chunk.get("error_text")

        if error_code or error_text:
            return "FAILURE"

        return "SUCCESS"

    """
    Creates a chunk text that is suitable for embedding.
    This helper function Creates chunk text that is enriched with embedding-friendly representation 
    of the original text.
    
    Args:
        chunk (Dict[str, str]): A dictionary containing chunk information.

    Returns:
        str: A formatted string suitable for embedding.
        
    """
    # Helper function
    # Creates chunk text that is enriched with embedding-friendly representation
    # of the original text.

    def _build_chunk_text_enriched(self, chunk: Dict[str, str]):
        messages = " ".join(
            msg.replace("OTHER::", "") for msg in chunk.get("messages", [])
        )
        error_code = chunk.get("error_code") or "No Error Code"
        error_text = chunk.get("error_text") or "No Error Text"

        call_status = self._derive_call_status(chunk)

        return (
            f"SIP Call Flow Event :: \n "
            f"Event Type: {chunk['type']}, \n "
            f"Messages: {messages}, \n "
            f"Call Status: {call_status}, \n "
            f"Error: {error_text}, \n "
            f"Error Code: {error_code}, \n "
            f"Session Duration: {chunk['session_duration_sec']} seconds,\n"
        )
