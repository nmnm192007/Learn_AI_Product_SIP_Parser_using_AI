import uuid
from typing import Dict, List


class Chunker:
    """
    Responsible for converting parsed SIP sessions into LLM-friendly chunks.
    """

    def __init__(self, max_messages_per_chunk: int = 5):
        self.max_messages = max_messages_per_chunk

    def chunk_sessions(self, sessions: List[Dict]) -> List[Dict]:
        """
        Main entry point
        """
        all_chunks = []

        for session in sessions:
            call_id = session.get("call_id")
            messages = session.get("messages", [])

            chunks = self._chunk_single_session(call_id, messages)
            all_chunks.extend(chunks)

        return all_chunks

    def _chunk_single_session(self, call_id: str, messages: List[Dict]) -> List[Dict]:
        """
        Break one SIP session into chunks
        """
        chunks = []
        current_chunk = []
        chunk_index = 1

        for msg in messages:
            current_chunk.append(msg)

            if len(current_chunk) >= self.max_messages:
                chunks.append(self._build_chunk(call_id, chunk_index, current_chunk))
                current_chunk = []
                chunk_index += 1

        # leftover messages
        if current_chunk:
            chunks.append(self._build_chunk(call_id, chunk_index, current_chunk))

        return chunks

    def _build_chunk(self, call_id: str, index: int, messages: List[Dict]) -> Dict:
        """
        Build chunk metadata
        """
        return {
            "chunk_id": f"{call_id}_{index}_{uuid.uuid4().hex[:6]}",
            "call_id": call_id,
            "messages": messages,
            "summary_hint": self._generate_summary_hint(messages)
        }

    def _generate_summary_hint(self, messages: List[Dict]) -> str:
        """
        Lightweight semantic hint (VERY IMPORTANT for retrieval later)
        """
        if not messages:
            return "empty"

        start = messages[0].get("type", "unknown")
        end = messages[-1].get("type", "unknown")

        return f"{start} → {end}"