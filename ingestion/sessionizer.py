"""
Arranges Call-ID-Based dict group
"""

from datetime import datetime

TRANSITIONS = {
    "IDLE":{"INVITE":"INIT"},
    "INIT":{"100 TRYING":"EARLY", "180 RINGING":"EARLY",
            "200 OK":"ESTABLISHED"},
    "EARLY":{"180 RINGING":"EARLY", "200 OK":"ESTABLISHED"},
    "ESTABLISHED":{"ACK":"CONFIRMED"},
    "CONFIRMED":{"UPDATE":"CONFIRMED", "BYE":"TERMINATED"},
    "TERMINATED":{},
}


class Sessionizer:

    def __init__(self):
        self.sessions = {}

    def process(self, msg):

        call_id = msg["call_id"]

        if call_id not in self.sessions:
            self.sessions[call_id] = self._create_session(call_id, msg)

        session = self.sessions[call_id]

        sip_msg = msg.get("sip_msg", "").strip().upper()

        # ---- Update messages ----
        session["messages"].append(sip_msg)

        # ---- FSM Update ----
        current_state = session["call_state"]
        session["call_state"] = TRANSITIONS.get(current_state, {}).get(
                sip_msg, current_state
        )

        # ---- Error Handling ----
        if sip_msg.startswith("OTHER::4") or sip_msg.startswith("OTHER::5"):
            session["has_error"] = True

            code = sip_msg.split("::")[1].split()[0]

            session["errors"].append({"code":code, "reason":sip_msg})

        # ---- Termination ----
        if sip_msg == "BYE":
            session["terminated"] = True
            session["end_time"] = msg["timestamp"]

        # ---- Update last seen ----
        session["last_seen"] = msg["timestamp"]

        # ---- Compute derived fields (AT END) ----
        session["duration_sec"] = self._compute_duration(session)
        session["final_status"] = self._derive_final_status(session)
        session["flow_valid"] = self._validate_flow(session)

        return session

    # ----------------------------------------

    def _create_session(self, call_id, msg):
        return {
            "call_id":call_id,
            "type_of_call":"CALL" if msg.get(
                "sip_msg") != "OPTIONS" else "KEEPALIVE",
            "call_state":"IDLE",
            "final_status":"UNKNOWN",
            "has_error":False,
            "terminated":False,
            "flow_valid":True,
            "start_time":msg["timestamp"],
            "end_time":None,
            "last_seen":msg["timestamp"],
            "duration_sec":0,
            "messages":[],
            "errors":[],
        }

    # ----------------------------------------

    def _compute_duration(self, session):
        try:
            fmt = "%Y-%m-%dT%H:%M:%S.%f"
            start = datetime.strptime(session["start_time"], fmt)
            end = datetime.strptime(session["last_seen"], fmt)
            return (end - start).total_seconds()
        except:
            return 0

    # ----------------------------------------

    def _derive_final_status(self, session):

        if session["type_of_call"] != "CALL":
            return "NON_CALL"

        if session["has_error"] and session["terminated"]:
            return "COMPLETED_WITH_ERRORS"

        if session["has_error"]:
            return "FAILED"

        if session["terminated"]:
            return "SUCCESS"

        return "INCOMPLETE"

    # ----------------------------------------

    def _validate_flow(self, session):

        msgs = session["messages"]

        # Basic validation rules
        if "200 OK" in msgs and "ACK" not in msgs:
            return False

        if "INVITE" not in msgs:
            return False

        return True

    # -----------------------------------------

    def get_sessions(self):
        return self.sessions
