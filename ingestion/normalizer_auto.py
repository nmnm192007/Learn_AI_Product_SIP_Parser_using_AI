from datetime import datetime
from typing import Dict, List


class Normalizer:
    """
    Responsible for cleaning and standardizing parsed SIP messages.
    """

    def normalize(self, messages: List[Dict]) -> List[Dict]:
        normalized = []

        for msg in messages:
            clean_msg = {
                "method": self._normalize_method(msg),
                "timestamp": self._normalize_timestamp(msg),
                "headers": self._normalize_headers(msg.get("headers", {})),
                "direction": self._infer_direction(msg),
                "call_id": self._extract_call_id(msg),
                "raw": msg.get("raw", ""),
            }

            normalized.append(clean_msg)

        return normalized

    # --------------------------
    # FIELD NORMALIZATION
    # --------------------------

    def _normalize_method(self, msg: Dict) -> str:
        """
        Normalize SIP method / response
        """
        method = msg.get("method") or msg.get("type") or ""

        method = method.upper().strip()

        # Normalize common variants
        mapping = {
            "INVITE": "INVITE",
            "ACK": "ACK",
            "BYE": "BYE",
            "CANCEL": "CANCEL",
            "REGISTER": "REGISTER",
            "OPTIONS": "OPTIONS",
            "200 OK": "200",
            "180 RINGING": "180",
            "100 TRYING": "100",
        }

        return mapping.get(method, method)

    def _normalize_timestamp(self, msg: Dict) -> str:
        """
        Convert timestamp to ISO format
        """
        ts = msg.get("timestamp")

        if not ts:
            return ""

        try:
            # Example: already datetime
            if isinstance(ts, datetime):
                return ts.isoformat()

            # Example: string parsing
            return datetime.fromisoformat(ts).isoformat()

        except Exception:
            return ""

    def _normalize_headers(self, headers: Dict) -> Dict:
        """
        Normalize header keys (case-insensitive)
        """
        normalized_headers = {}

        for k, v in headers.items():
            normalized_headers[k.lower()] = v.strip() if isinstance(v, str) else v

        return normalized_headers

    def _infer_direction(self, msg: Dict) -> str:
        """
        Infer call direction (basic heuristic)
        """
        raw = msg.get("raw", "").lower()

        if "received" in raw:
            return "INBOUND"
        elif "sent" in raw:
            return "OUTBOUND"

        return "UNKNOWN"

    def _extract_call_id(self, msg: Dict) -> str:
        """
        Extract Call-ID from headers
        """
        headers = msg.get("headers", {})
        return headers.get("call-id", "")
