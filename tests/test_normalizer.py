import os
from dotenv import load_dotenv
from pathlib import Path

from ingestion.parser import read_logs, parse_log_segment
from ingestion.normalizer import Normalizer

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
LOG_FILE = os.getenv("LOG_FILE")

# Step 1 : Get path of log_file
log_file = BASE_DIR / LOG_FILE

def test_direction():
	normalizer = Normalizer()
	testmsg = {
		"timestamp":"2026-03-30 22:55:35,621",
		"direction":"Received",
		"sip_msg":"INVITE",
		"from":"a",
		"to":"b",
		"call_id":"123",
		"content_length":"10"
	}
	result = normalizer.normalize(testmsg)
	# print(result)
	assert result["direction"] == "IN"
	assert result["direction"] in ("IN","OUT"), cleaned_msg
	assert result["call_id"]

def test_bad_format_msg():
	normalizer = Normalizer()
	test_msg = {
		"timestamp":"",
		"direction":"Random",
		"sip_msg":"HELLO",
		"from":"",
		"to":"",
		"call_id":"",
		"content_length":""
	}
	assert test_msg["direction"] in ("IN","OUT"), test_msg
	assert test_msg["timestamp"] != "", test_msg

	print(normalizer.normalize(test_msg))


#         DON'T USE THE BELOW 
# if __name__ == "__main__":
# 	# test_direction()
# 	test_bad_format_msg()
