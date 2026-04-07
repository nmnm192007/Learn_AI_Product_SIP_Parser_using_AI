"""
class Normalizer

"""
from datetime import datetime
from typing import Dict

class Normalizer:
	def __init__(self):
		self.cleaned_msg = {}

	def normalize(self, parsed_msg: dict) -> dict:
		if parsed_msg is None:
			return {}

		self.cleaned_msg["timestamp"] = self._normalize_time_stamp(parsed_msg["timestamp"])
		self.cleaned_msg["direction"] = self._normalize_direction(parsed_msg["direction"])
		self.cleaned_msg["sip_msg"] = self._normalize_headers(parsed_msg["sip_msg"])
		self.cleaned_msg["from"] = parsed_msg["from"].strip()
		self.cleaned_msg["to"] = parsed_msg["to"].strip()
		self.cleaned_msg["call_id"] = self._normalize_call_id(parsed_msg["call_id"])
		self.cleaned_msg["content_length"] = self._normalize_content_len(parsed_msg["content_length"])
			
		return self.cleaned_msg

	def _normalize_time_stamp(self, time_stamp):
		if isinstance(time_stamp, datetime):
			return time_stamp.isoformat()
		elif isinstance(time_stamp,str):
			d = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S,%f")
			return d.isoformat()

	def _normalize_direction(self, direction):
		if not isinstance(direction,str):
			return "default"
		if direction in ("Received","Sending"):
			return "IN" if direction == "Received" else "OUT"

	def _normalize_headers(self, headers):
		SIP_METHODS = ('INVITE', 'UPDATE', 'ACK', 'BYE', 'OPTIONS')
		SIP_RESPONSES = ('100 TRYING', '180 RINGING', '200 OK')
		if headers in SIP_METHODS:
			return headers.strip()
		elif headers in SIP_RESPONSES:
			return headers.strip()
		else:
			return "OTHER::" + headers
		return headers.strip()

	def _normalize_call_id(self, call_id):
		if not call_id or call_id == "":
			return "UNKNOWN::"+call_id
		return call_id.strip()

	def _normalize_content_len(self, content_len):
		if not content_len or content_len == "":
			return "INVALID::"+content_len
		else:
			return int(content_len.strip())



