"""
       Read the sip call flow log file and parse the message segments

       @:param
       @:param
       @:return:
"""

import os
from typing import Dict, Type, Any, Generator
from dotenv import load_dotenv
from pathlib import Path
from itertools import tee, islice

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent  # project root
LOG_FILE = os.getenv("LOG_FILE")
log_file = BASE_DIR / LOG_FILE


def read_logs(log_file: Path) -> Generator[str, Any, None]:
    """
    read the sip call flow log file and yield the generator
    :param log_file:
    :return:
    """

    if not log_file.exists():
        raise FileNotFoundError(f'{log_file} does not exist')

    with open(log_file, "r") as f:
        for gen in f:
            yield gen


def group_messages(log_gen: Generator[Any, Any, Any]) -> Generator[
    Any, Any, Any]:
    message = []

    for log_line in log_gen:
        if log_line.startswith("[") and message:
            yield "\n".join(message)
            message = []
        message.append(log_line.strip())

    if message:
        yield "\n".join(message)


def parse_log_segment(log_generator: Generator[str, None, None]) -> Dict[str,
Any]:
    """
    parse the sip call flow log file and parse the message segment
    :param log_generator:
    :return:
    """
    for msg in group_messages(log_generator):

        ret_dict: Dict[str, Any] = \
            {
                "timestamp":"",
                "direction":"",
                "sip_msg":"",
                "from":"",
                "to":"",
                "call_id":"",
                "content_length":""
            }

        lines = msg.split("\n")
        SIP_METHODS = ('INVITE', 'UPDATE', 'ACK', 'BYE', 'OPTIONS')

        for line in lines:
            if line.startswith("["):
                parts = line.split()
                ret_dict["timestamp"] = parts[0] + " " + parts[1]
                ret_dict["direction"] = parts[2]

            elif any(line.startswith(method) for method in SIP_METHODS):
                ret_dict["sip_msg"] = line.split()[0]

            elif line.startswith("SIP/2.0"):
                ret_dict["sip_msg"] = " ".join(line.split()[1:3])

            elif line.startswith("From:"):
                ret_dict["from"] = line.split(':', 1)[1].strip()

            elif line.startswith('To:'):
                ret_dict["to"] = line.split(":", 1)[1].strip()

            elif line.startswith('Call-ID:'):
                ret_dict["call_id"] = line.split(":", 1)[1].strip()

            elif line.startswith('Content-Length:'):
                ret_dict["content_length"] = line.split(":", 1)[1].strip()

        yield ret_dict
