"""
Arranges Call-ID-Based dict group
"""

from collections import defaultdict


class Sessionizer:

    def __init__(self):
        self.sessions = defaultdict(list)

    def process(self, msg: dict) -> None:
        """
        processes the normalized messages as sessions with state
        :param msg:
        :return:
        """
        call_id = msg.get("call_id")
        if not call_id or call_id.startswith("UNKNOWN"):
            return
        # self.sessions[call_id].append(msg) ## used for pre-state-m/c cases

        # Create session if not existing already
        if call_id not in self.sessions:
            self.sessions[call_id] = {
                "messages":[],
                "state":"INIT",
                "start_time":msg.get("timestamp"),
                "last_seen":msg.get("timestamp"),
            }
        session = self.sessions[call_id]

        #   Append Message
        session["messages"].append(msg)

        #  Update Last Seen
        session["last_seen"] = msg.get("timestamp")

        #  Update state
        session["state"] = self._next_state(session["state"], msg["sip_msg"])

    def get_sessions(self) -> dict[str, dict]:
        """
        prepares the dict that would be used in pipeline
        :return:   dict
        """
        return dict(self.sessions)

    def _next_state(self, current_state: str, sip_msg: str) -> str:
        """
        sets the next state as an str
        :param current_state:
        :param sip_msg:
        :return:
        """
        sip_msg = sip_msg.strip().upper()

        if sip_msg == "INVITE":
            return "INIT"

        elif sip_msg in ("100 TRYING", "180 RINGING"):
            return "EARLY"

        elif sip_msg == "200 OK":
            return "ESTABLISHED"

        elif sip_msg == "BYE":
            return "TERMINATED"

        elif sip_msg.startswith("OTHER::4") or sip_msg.startswith("OTHER::5"):
            return "ERROR"

        return "UNKNOWN"
