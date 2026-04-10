"""
Arranges Call-ID-Based dict group
"""

from collections import defaultdict
from datetime import datetime


class Sessionizer:

    def __init__(self):
        self.sessions = defaultdict(list)

    def process(self, msg: dict) -> None:
        """
        Core of the Sessionizer class
        Processes the normalized messages as sessions with state defined
        using the Finite State Machine
        :param msg: dict :: Normalized message passed from Normalizer
        :return: None
        """
        call_id = msg.get("call_id")
        if not call_id or call_id.startswith("UNKNOWN"):
            return
        # self.sessions[call_id].append(msg) ## used for pre-state-m/c cases

        # Create session if not existing already
        if call_id not in self.sessions:
            self.sessions[call_id] = {
                "messages": [],
                "call_state": "INIT",
                "type_of_call": "UNKNOWN",
                "has_error": False,
                "terminated": False,
                "start_time": msg.get("timestamp"),
                "last_seen": msg.get("timestamp"),
                "final_status": "",
                "duration": 0,
            }
        session = self.sessions[call_id]

        #   Append Message
        session["messages"].append(msg)

        #  Update Last Seen
        session["last_seen"] = msg.get("timestamp")

        #  Update Call state
        sip_msg = msg["sip_msg"]
        #  Call progression
        session["call_state"] = self._update_call_state(session["call_state"], sip_msg)
        # Error Tracking
        if sip_msg.startswith("OTHER::4") or sip_msg.startswith("OTHER::5"):
            session["has_error"] = True
        # Termination
        if sip_msg == "BYE":
            session["terminated"] = True

        # set type_of_call
        if sip_msg == "INVITE":
            session["type_of_call"] = "CALL"
        elif sip_msg == "OPTIONS":
            session["type_of_call"] = "KEEPALIVE"
        # call_state for OPTIONS to be NA
        if session["type_of_call"] != "CALL":
            session["call_state"] = "NA"

        # Get final status
        session["final_status"] = self._derive_final_status(session)

        # Get total duration
        session["duration"] = self._compute_actual_duration(session)

    def _update_call_state(self, current_state: str, sip_msg: str) -> str:
        """
        updates the call state corresponding to the call flow behaviour in
        mid-call phase
        Works independently as a FINITE STATE MACHINE (FSM)
        :param call_state:
        :param sip_msg:
        :return: updated_call_state:str
        """
        sip_msg = sip_msg.strip().upper()
        if sip_msg == "INVITE":
            return "INIT"
        elif sip_msg in ("100 TRYING", "180 RINGING"):
            if current_state in ("INIT", "EARLY"):
                return "EARLY"
        elif sip_msg in ("200 OK"):
            return "ESTABLISHED"
        elif sip_msg == "ACK":
            if current_state == "ESTABLISHED":
                return "CONFIRMED"
        elif sip_msg == "UPDATE":
            if current_state == "CONFIRMED":
                return "CONTINUED"
        elif sip_msg == "BYE":
            return "TERMINATED"
        elif sip_msg.startswith("OTHER::4"):
            return "TEMPORARY ERROR : Probably USER ERROR"
        elif sip_msg.startswith("OTHER::5"):
            return "PERMANENTLY ERROR : Probably SYSTEM ERROR"
        return current_state

    def _derive_final_status(self, session: defaultdict[str, dict[str, str]]) -> str:
        """
        From the parameters tyoe of call, has_error and terminated, derive
        the final status of the SIP CALL and print it
        :param session: defaultdict[str, dict[str, str]]
        :return: Final Status : str
        """
        if session["type_of_call"] != "CALL":
            return "NON CALL"
        if session["has_error"] and session["terminated"]:
            return "COMPLETED WITH ERRORS"
        if session["has_error"]:
            return "FAILED"
        if session["terminated"]:
            return "SUCCEEDED"
        return "CALL NOT COMPLETE"

    def _compute_actual_duration(
        self, session: defaultdict[str, dict[str, str]]
    ) -> datetime:
        """
        calculate the actual duration of the session
        :param session: defaultdict[str, dict[str, str]]
        :return: duration in seconds
        """
        start_sec = datetime.strptime(session["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
        end_sec = datetime.strptime(session["last_seen"], "%Y-%m-%dT%H:%M:%S.%f")
        duration_sec = (end_sec - start_sec).total_seconds()
        return duration_sec

    def get_sessions(self) -> dict[str, dict]:
        """
        prepares the dict that would be used in pipeline
        :return:   dict
        """
        return dict(self.sessions)
