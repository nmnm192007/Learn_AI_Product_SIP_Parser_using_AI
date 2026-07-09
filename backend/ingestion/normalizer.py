"""
class Normalizer

"""

from datetime import datetime


class Normalizer:
    def __init__(self):
        self.cleaned_msg = {}

    def normalize(self, parsed_msg: dict) -> dict:
        """
        normalize the message
        :param parsed_msg: dict
        :return:dict
        """
        if parsed_msg is None:
            return {}

        cleaned_msg = {}

        cleaned_msg["timestamp"] = self._normalize_time_stamp(parsed_msg["timestamp"])
        cleaned_msg["direction"] = self._normalize_direction(parsed_msg["direction"])
        cleaned_msg["sip_msg"] = self._normalize_headers(parsed_msg["sip_msg"])
        cleaned_msg["from"] = parsed_msg["from"].strip()
        cleaned_msg["to"] = parsed_msg["to"].strip()
        cleaned_msg["call_id"] = self._normalize_call_id(parsed_msg["call_id"])
        cleaned_msg["content_length"] = self._normalize_content_len(
            parsed_msg["content_length"]
        )

        return cleaned_msg

    def _normalize_time_stamp(self, time_stamp: datetime or str) -> datetime:
        """
        normalize the time stamp
        :param time_stamp: datetime or str
        :return: datetime
        """
        try:
            if isinstance(time_stamp, datetime):
                return time_stamp.isoformat()
            elif isinstance(time_stamp, str):
                d = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S,%f")
                return d.isoformat()
        except Exception as e:
            return "INVALID time stamp ::" + time_stamp + " " + e

    def _normalize_direction(self, direction: str) -> str:
        """
        normalize the direction
        :param direction: str
        :return: str
        """
        if not isinstance(direction, str):
            return "default"
        if direction in ("Received", "Sending"):
            return "IN" if direction == "Received" else "OUT"
        else:
            return "UNKNOWN Direction ::" + direction

    def _normalize_headers(self, headers: str) -> str:
        """
        normalize the headers
        :param headers: str
        :return: str
        """
        SIP_METHODS = ("INVITE", "UPDATE", "ACK", "BYE", "OPTIONS")
        SIP_RESPONSES = ("100 TRYING", "180 RINGING", "200 OK")
        if headers in SIP_METHODS or headers in SIP_RESPONSES:
            return headers.strip()
        else:
            return "OTHER::" + headers

    def _normalize_call_id(self, call_id: str) -> str:
        """
        normalize the call id
        :param call_id: str
        :return: str
        """
        if not call_id or call_id == "":
            return "UNKNOWN::" + call_id
        return call_id.strip()

    def _normalize_content_len(self, content_len: str) -> int:
        """
        normalize the content length
        :param content_len: str
        :return: str
        """
        if not content_len or content_len == "":
            return "INVALID::" + content_len
        else:
            return content_len.strip()
