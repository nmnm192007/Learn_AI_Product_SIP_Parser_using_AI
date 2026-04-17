import unittest

from ingestion.chunk_sessions import ChunkSession


class TestChunkSession(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.chunk_session = ChunkSession()

    def test_get_phase_initial(self):
        """Test _get_phase method for INITIAL phase."""
        self.assertEqual(self.chunk_session._get_phase("INVITE"), "INITIAL")

    def test_get_phase_setup(self):
        """Test _get_phase method for SETUP phase."""
        self.assertEqual(self.chunk_session._get_phase("100 TRYING"), "SETUP")
        self.assertEqual(self.chunk_session._get_phase("180 RINGING"), "SETUP")
        self.assertEqual(self.chunk_session._get_phase("200 OK"), "SETUP")

    def test_get_phase_established(self):
        """Test _get_phase method for ESTABLISHED phase."""
        self.assertEqual(self.chunk_session._get_phase("ACK"), "ESTABLISHED")
        self.assertEqual(self.chunk_session._get_phase("UPDATE"), "ESTABLISHED")

    def test_get_phase_terminated(self):
        """Test _get_phase method for TERMINATED phase."""
        self.assertEqual(self.chunk_session._get_phase("BYE"), "TERMINATED")

    def test_get_phase_error(self):
        """Test _get_phase method for ERROR phase."""
        self.assertEqual(self.chunk_session._get_phase("OTHER::ERROR"), "ERROR")
        self.assertEqual(self.chunk_session._get_phase("OTHER::TIMEOUT"), "ERROR")

    def test_get_phase_keepalive(self):
        """Test _get_phase method for KEEPALIVE phase."""
        self.assertEqual(self.chunk_session._get_phase("OPTIONS"), "KEEPALIVE")

    def test_get_phase_unknown(self):
        """Test _get_phase method for UNKNOWN phase."""
        self.assertEqual(self.chunk_session._get_phase("UNKNOWN_MSG"), "UNKNOWN")

    def test_create_chunk(self):
        """Test _create_chunk method."""
        messages = ["INVITE", "100 TRYING"]
        result = self.chunk_session._create_chunk("call_001", "1", "INITIAL", messages)

        expected = {
            "chunk_id": "call_001_1",
            "type": "INITIAL",
            "messages": ["INVITE", "100 TRYING"],
        }
        self.assertEqual(result, expected)

    def test_create_chunk_message_copy(self):
        """Test that _create_chunk creates a copy of messages list."""
        messages = ["INVITE"]
        result = self.chunk_session._create_chunk("call_001", "1", "INITIAL", messages)

        # Modify original list
        messages.append("NEW_MSG")

        # Result should not be affected
        self.assertEqual(result["messages"], ["INVITE"])

    def test_chunk_sessions_func_simple_flow(self):
        """Test chunk_sessions_func with a simple call flow."""
        sessions = {
            "call_001": {"messages": ["INVITE", "100 TRYING", "200 OK", "ACK", "BYE"]}
        }

        result = self.chunk_session.chunk_sessions_func(sessions)

        self.assertIn("call_001", result)
        chunks = result["call_001"]
        self.assertEqual(len(chunks), 4)  # INITIAL, SETUP, ESTABLISHED, TERMINATED

        # Check first chunk (INITIAL)
        self.assertEqual(chunks[0]["type"], "INITIAL")
        self.assertEqual(chunks[0]["messages"], ["INVITE"])

        # Check second chunk (SETUP)
        self.assertEqual(chunks[1]["type"], "SETUP")
        self.assertEqual(chunks[1]["messages"], ["100 TRYING", "200 OK"])

        # Check third chunk (ESTABLISHED)
        self.assertEqual(chunks[2]["type"], "ESTABLISHED")
        self.assertEqual(chunks[2]["messages"], ["ACK"])

        # Check fourth chunk (TERMINATED)
        self.assertEqual(chunks[3]["type"], "TERMINATED")
        self.assertEqual(chunks[3]["messages"], ["BYE"])

    def test_chunk_sessions_func_with_error(self):
        """Test chunk_sessions_func with error messages."""
        sessions = {"call_001": {"messages": ["INVITE", "OTHER::ERROR", "100 TRYING"]}}

        result = self.chunk_session.chunk_sessions_func(sessions)
        chunks = result["call_001"]

        self.assertEqual(len(chunks), 3)

        # First chunk should be INITIAL
        self.assertEqual(chunks[0]["type"], "INITIAL")
        self.assertEqual(chunks[0]["messages"], ["INVITE"])

        # Second chunk should be ERROR (isolated)
        self.assertEqual(chunks[1]["type"], "ERROR")
        self.assertEqual(chunks[1]["messages"], ["OTHER::ERROR"])

        # Third chunk should be SETUP
        self.assertEqual(chunks[2]["type"], "SETUP")
        self.assertEqual(chunks[2]["messages"], ["100 TRYING"])

    def test_chunk_sessions_func_with_keepalive(self):
        """Test chunk_sessions_func with keepalive messages."""
        sessions = {"call_001": {"messages": ["INVITE", "OPTIONS", "100 TRYING"]}}

        result = self.chunk_session.chunk_sessions_func(sessions)
        chunks = result["call_001"]

        self.assertEqual(len(chunks), 2)

        # First chunk should be INITIAL
        self.assertEqual(chunks[0]["type"], "INITIAL")
        self.assertEqual(chunks[0]["messages"], ["INVITE"])

        # Second chunk should be KEEPALIVE then SETUP
        self.assertEqual(chunks[1]["type"], "SETUP")
        self.assertEqual(chunks[1]["messages"], ["OPTIONS", "100 TRYING"])

    def test_chunk_sessions_func_empty_session(self):
        """Test chunk_sessions_func with empty messages."""
        sessions = {"call_001": {"messages": []}}

        result = self.chunk_session.chunk_sessions_func(sessions)

        self.assertIn("call_001", result)
        self.assertEqual(result["call_001"], [])

    def test_chunk_sessions_func_multiple_calls(self):
        """Test chunk_sessions_func with multiple call sessions."""
        sessions = {
            "call_001": {"messages": ["INVITE", "200 OK", "ACK"]},
            "call_002": {"messages": ["INVITE", "BYE"]},
        }

        result = self.chunk_session.chunk_sessions_func(sessions)

        self.assertIn("call_001", result)
        self.assertIn("call_002", result)

        # Check call_001 has 3 chunks
        self.assertEqual(len(result["call_001"]), 3)

        # Check call_002 has 2 chunks
        self.assertEqual(len(result["call_002"]), 2)

    def test_chunk_sessions_func_chunk_ids(self):
        """Test that chunk IDs are correctly incremented."""
        sessions = {"call_001": {"messages": ["INVITE", "100 TRYING", "ACK", "BYE"]}}

        result = self.chunk_session.chunk_sessions_func(sessions)
        chunks = result["call_001"]

        expected_chunk_ids = ["call_001_1", "call_001_2", "call_001_3", "call_001_4"]
        actual_chunk_ids = [chunk["chunk_id"] for chunk in chunks]

        self.assertEqual(actual_chunk_ids, expected_chunk_ids)

    def test_chunk_sessions_func_same_phase_messages(self):
        """Test handling of consecutive messages in the same phase."""
        sessions = {"call_001": {"messages": ["100 TRYING", "180 RINGING", "200 OK"]}}

        result = self.chunk_session.chunk_sessions_func(sessions)
        chunks = result["call_001"]

        # Should create only one chunk since all messages are SETUP phase
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["type"], "SETUP")
        self.assertEqual(chunks[0]["messages"], ["100 TRYING", "180 RINGING", "200 OK"])

    def test_result_initialization(self):
        """Test that result is properly initialized."""
        # First call
        sessions1 = {"call_001": {"messages": ["INVITE"]}}
        result1 = self.chunk_session.chunk_sessions_func(sessions1)

        # Second call should reset result
        sessions2 = {"call_002": {"messages": ["BYE"]}}
        result2 = self.chunk_session.chunk_sessions_func(sessions2)

        # Result should only contain call_002
        self.assertIn("call_002", result2)
        self.assertNotIn("call_001", result2)


if __name__ == "__main__":
    unittest.main()
