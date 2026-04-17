from typing import Dict, List


class ChunkSession:
    def __init__(self) -> None:
        self.result = {}

    def _create_chunk(
        self, call_id: str, chunk_id: str, chunk_type: str, messages: List
    ) -> Dict[str, str]:
        """
        _create_chunk helper function to create chunks
        :param call_id: str
        :param chunk_id: str
        :param chunk_type: str
        :param messages: List[str]
        :return: Dict[str, str]
        """

        return {
            "chunk_id": f"{call_id}_{chunk_id}",
            "type": f"{chunk_type}",
            "messages": messages.copy(),
        }

    def _get_phase(self, msg: str) -> str:
        """
        helper function to get phase
        :param msg: str
        :return: str
        """

        if msg == "INVITE":
            return "SETUP"
        elif msg in ["100 TRYING", "180 RINGING", "200 OK"]:
            return "SETUP"
        elif msg in ["ACK", "UPDATE"]:
            return "ESTABLISHED"
        elif msg == "BYE":
            return "TERMINATED"
        elif "OTHER::" in msg:
            return "ERROR"
        elif msg == "OPTIONS":
            return "KEEPALIVE"
        else:
            return "UNKNOWN"

    def chunk_sessions_func(self, sessions: Dict[str, str]) -> Dict[str, str]:
        """
        chunk_sessions_func implements CHUNKING
        :param sessions: Dict[str, str]
        :return: result: Dict[str, str]
        """
        self.result = {}

        for call_id, session in sessions.items():
            chunks = []
            current_chunk = []
            current_phase = None
            chunk_id = 0
            messages = session["messages"]

            for msg in messages:
                phase = self._get_phase(msg)

                # ERROR Handling (ISOLATED on purpose)
                if phase == "ERROR":
                    if current_chunk:
                        chunk_id = chunk_id + 1
                        chunks.append(
                            self._create_chunk(
                                call_id, chunk_id, current_phase, current_chunk
                            )
                        )
                        current_chunk = []

                    chunk_id = chunk_id + 1
                    chunks.append(self._create_chunk(call_id, chunk_id, "ERROR", [msg]))
                    continue

                # check KeepAlive
                if phase == "KEEPALIVE":
                    current_phase = "KEEPALIVE"

                # First Message
                if current_phase is None:
                    current_phase = phase

                # Phase Changes
                elif current_phase != phase:
                    if current_chunk:
                        chunk_id = chunk_id + 1
                        chunks.append(
                            self._create_chunk(
                                call_id, chunk_id, current_phase, current_chunk
                            )
                        )
                    current_phase = phase
                    current_chunk = []

                # Append ONLY after decisions taken on full run iteration
                current_chunk.append(msg)

            # separate addition of FINAL CHUNK from the sequence/pattern
            if current_chunk:
                chunk_id = chunk_id + 1
                chunks.append(
                    self._create_chunk(call_id, chunk_id, current_phase, current_chunk)
                )
            self.result[call_id] = chunks

        return self.result
