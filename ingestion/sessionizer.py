"""
Arranges Call-ID-Based dict group
"""

from datetime import datetime
from typing import Dict

"""
Defines the Finite State Machine FSM as a dict[str,dict[str:str]]
"""

TRANSITIONS = {
    "IDLE":{"INVITE":"INIT"},
    "INIT":{
        "100 TRYING":"EARLY",
        "180 RINGING":"EARLY",
        "200 OK":"ESTABLISHED",
    },
    "EARLY":{
        "180 RINGING":"EARLY",
        "200 OK":"ESTABLISHED",
    },
    "ESTABLISHED":{
        "ACK":"CONFIRMED",
    },
    "CONFIRMED":{
        "UPDATE":"CONFIRMED",
        "BYE":"TERMINATED",
    },
    "TERMINATED":{},
}


# ------------------------------------------------


class Sessionizer:
    """
    Class that constructs sessions meaningfully
    """

    def __init__(self):
        self.sessions = {}

    # ----------------------------------------

    def process(self, msg: Dict[str, str]) -> Dict[str:Any]:
        """
        Core of the Sessionizer class
        Processes the normalized messages as sessions with state defined
        using the Finite State Machine

        :param msg: Dict[str, str] :: Normalized message passed from Normalizer
        :return: Dict[str, Any]
        """

        # Segregate call_id

        call_id = msg["call_id"]
        if not call_id or call_id.startswith("UNKNOWN"):
            return
        if call_id not in self.sessions:
            self.sessions[call_id] = self._create_session(call_id, msg)
        # self.sessions[call_id].append(msg) ## used for pre-state-m/c cases

        session = self.sessions[call_id]

        sip_msg = msg.get("sip_msg", "").strip().upper()
        if sip_msg == "OPTIONS":
            session["type_of_call"] = "KEEPALIVE"

        # ---- Update messages ----
        session["messages"].append(sip_msg)
        if session["type_of_call"] != "CALL":
            session["call_state"] = "NA"

        # ---- Update last seen ----
        session["last_seen"] = msg["timestamp"]

        # ---- Compute derived fields (AT END) ----
        session["duration_sec"] = self._compute_duration(session)
        session["final_status"] = self._derive_final_status(session)
        session["flow_valid"] = self._validate_flow(session)

        # ---- FSM Update ----
        if session["call_state"] == "CALL":
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

        return session

    # ----------------------------------------

    def _create_session(self, call_id: str, msg: Dict[str, str]) -> Dict[
        str, Any]:
        """
        Create a new session from the normalized message
        :param call_id: str
        :param msg: Dict[str, str] :: Normalized message passed from Normalizer
        :return: session: Dict[str, Any]
        """
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

    def _compute_duration(self, session: Dict[str, str]) -> float:
        """
        calculate the actual duration of the session
        :param session: Dict[str, str]
        :return: duration in seconds : float
        """
        try:
            fmt = "%Y-%m-%dT%H:%M:%S.%f"
            start = datetime.strptime(session["start_time"], fmt)
            end = datetime.strptime(session["last_seen"], fmt)
            return (end - start).total_seconds()
        except:
            return 0

    # ----------------------------------------

    def _derive_final_status(self, session: Dict[str, str]) -> str:
        """
        From the parameters tyoe of call, has_error and terminated, derive
        the final status of the SIP CALL and print it
        :param session: Dict[str, str]
        :return: str
        """

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

    def _validate_flow(self, session: Dict[str, str]) -> bool:
        """
        Validate the session flow
        :param session: Dict[str, str]
        :return:bool
        """
        msgs = session["messages"]

        # Basic validation rules
        if "200 OK" in msgs and "ACK" not in msgs:
            return False

        if "INVITE" not in msgs:
            return False

        return True

    # -----------------------------------------

    def get_sessions(self):
        """
        Get all sessions in the instance object
        :return:sessions: Dict[str, str]
        """
        return self.sessions
