"""
Arranges Call-ID-Based dict group
"""

from collections import defaultdict


class Sessionizer:
	def __init__(self):
		self.sessions = defaultdict(list)

	def process(self, msg: dict):
		call_id = msg.get("call_id")
		if not call_id:
			return
		self.sessions[call_id].append(msg)

	def get_sessions(self):
		return dict(self.sessions)
