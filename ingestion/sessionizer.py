from typing import List, Dict
from collections import defaultdict


class Sessionizer:
    """
    Groups normalized SIP messages into sessions based on Call-ID.
    """

    def __init__(self):
        pass

    def create_sessions(self, messages: List[Dict]) -> List[Dict]:
        """
        Main entry point
        """
        sessions = defaultdict(list)

        for msg in messages:
            call_id = msg.get("call_id")

            # Handle missing call-id
            if not call_id:
                call_id = self._fallback_call_id(msg)

            sessions[call_id].append(msg)

        # Sort messages inside each session
        final_sessions = []

        for call_id, msgs in sessions.items():
            sorted_msgs = self._sort_by_timestamp(msgs)

            session = {
                "call_id": call_id,
                "messages": sorted_msgs,
                "message_count": len(sorted_msgs),
                "start_time": sorted_msgs[0].get("timestamp") if sorted_msgs else None,
                "end_time": sorted_msgs[-1].get("timestamp") if sorted_msgs else None
            }

            final_sessions.append(session)

        return final_sessions

    # --------------------------
    # HELPERS
    # --------------------------

    def _sort_by_timestamp(self, messages: List[Dict]) -> List[Dict]:
        """
        Ensure chronological order
        """
        return sorted(messages, key=lambda x: x.get("timestamp") or "")

    def _fallback_call_id(self, msg: Dict) -> str:
        """
        Generate fallback ID if Call-ID missing
        """
        raw = msg.get("raw", "")
        timestamp = msg.get("timestamp", "")

        return f"fallback_{hash(raw + timestamp)}"