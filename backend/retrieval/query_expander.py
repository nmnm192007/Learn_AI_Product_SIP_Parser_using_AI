import re
from typing import Dict, List


class QueryExpander:
    """
    Deterministic query expansion for SIP log retrieval.

    No LLM is used here.

    The purpose is to convert a user's natural-language question
    into retrieval-friendly terminology while preserving the
    original query.
    """

    PHRASE_SYNONYMS: Dict[str, str] = {
        "transaction does not exist": "481 CALL LEG TRANSACTION DOES NOT EXIST",
        "internal server error": "500 INTERNAL SERVER ERROR",
        "server error": "500 INTERNAL SERVER ERROR",
        "call flows": "SIP CALL FLOW",
        "call flow": "SIP CALL FLOW",
        "call leg": "CALL LEG",
    }

    TERM_SYNONYMS: Dict[str, List[str]] = {
        "failure": [
            "failure",
            "failed",
            "fail",
            "error",
            "problem",
            "issue",
        ],
        "error": [
            "error",
            "failure",
            "fault",
            "problem",
            "issue",
        ],
        "reason": [
            "reason",
            "cause",
            "root cause",
            "why",
        ],
        "call": [
            "call",
            "SIP call",
            "call flow",
            "session",
        ],
        "flow": [
            "flow",
            "call flow",
            "SIP flow",
            "signaling",
        ],
        "terminate": [
            "terminate",
            "termination",
            "terminated",
            "BYE",
        ],
        "timeout": [
            "timeout",
            "timed out",
            "timing",
        ],
    }

    KEYWORDS = {
        "failure",
        "fail",
        "failed",
        "error",
        "issue",
        "problem",
        "reason",
        "cause",
        "why",
        "call",
        "calls",
        "flow",
        "flows",
        "sip",
        "terminate",
        "terminated",
        "termination",
        "timeout",
        "timed",
    }

    def expand(self, query: str) -> Dict:
        """
        Expand a query into retrieval-friendly terminology.
        Also detect the intent of the query.
        :param query:
        :return:
        """

        original_query = query.strip()
        phrases = self._find_phrases(original_query)
        terms = self._find_terms(original_query)
        concepts = phrases + terms

        if concepts:
            expanded_query = " ".join(test for test in concepts)
        else:
            expanded_query = original_query

        return {
            "original_query": original_query,
            "expanded_query": expanded_query,
        }

    def _find_phrases(self, query: str) -> list[str]:
        """
        Find phrases in a query.
        :param query:
        :return:
        """
        query_lower = query.lower()

        matched = []

        phrases = sorted(
            self.PHRASE_SYNONYMS.keys(),
            key=len,
            reverse=True,
        )

        for phrase in phrases:
            if re.search(
                rf"\b{re.escape(phrase)}\b",
                query_lower,
            ):
                matched.append(self.PHRASE_SYNONYMS[phrase])

        return matched

    def _find_terms(self, query: str) -> list[str]:
        """
        Find terms in a query.
        :param query:
        :return:
        """
        query_lower = query.lower()

        matched = []

        for term, canonical in self.TERM_SYNONYMS.items():
            if re.search(
                rf"\b{re.escape(term)}\b",
                query_lower,
            ):
                matched.extend(canonical)

        return matched

    @staticmethod
    def _detect_intent(tokens: List[str]) -> str:
        """
        Detect the intent of a query.
        :param tokens:
        :return:
        """
        has_failure = any(
            word in tokens
            for word in [
                "failure",
                "fail",
                "failed",
                "error",
                "issue",
                "problem",
            ]
        )

        has_reason = any(
            word in tokens
            for word in [
                "reason",
                "cause",
                "why",
            ]
        )

        has_flow = any(
            word in tokens
            for word in [
                "call",
                "flow",
                "flows",
                "sip",
            ]
        )

        has_termination = any(
            word in tokens
            for word in [
                "terminate",
                "terminated",
                "termination",
            ]
        )

        if has_failure and has_reason:
            return "FAILURE_REASON"

        if has_failure:
            return "FAILURE_ANALYSIS"

        if has_termination:
            return "TERMINATION_ANALYSIS"

        if has_flow:
            return "CALL_FLOW_ANALYSIS"

        return "GENERAL"
