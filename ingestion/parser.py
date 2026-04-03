"""
       Read the sip call flow log file and parse the message segments

       @:param
       @:param
       @:return:
"""

import os
from typing import Type, Any, Generator
from dotenv import load_dotenv
from pathlib import Path
from itertools import tee, islice

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent  # project root
LOG_FILE = os.getenv("LOG_FILE")
log_file = BASE_DIR/LOG_FILE


def read_logs(log_file: Path) -> Generator[str, Any, None]:
    """
    Parse the log file
    :param log_file:
    :return:
    """

    try:
        with open(log_file, 'r') as f_obj:
            for gen in f_obj:
                yield gen
    except FileNotFoundError:
        raise FileNotFoundError("Log file not found, check LOG_FILE in .env")
    except IOError:
        raise IOError("Log file not found, check LOG_FILE in .env")
    except Exception as e:
        raise e


def parse_log_segment(log_generator: Generator[str, Any, None]) -> Dict[str,
Any]:
    """
    get the line from log file and parse the message segment
    :param line:
    :return:
    """
    ret_dict: Dict[str, Any] = {}
    time_stamp = msg_dir = sip_msg = from_hdr = to_hdr = call_id = \
        content_length = ""

    for line in log_generator:
        print("line: ", line)
        if not line:
            continue
        line = line.strip()
        if line.startswith((' ', '#')):
            return None
        try:
            if line.startswith('['):
                time_stamp = line.split(sep=" ")[0] if time_stamp else ""
                msg_dir = line.split(sep=" ")[1]
            if line.startswith(('INVITE', 'UPDATE',)):
                sip_msg = line.split(sep=" ")[0]
            if line.startswith(('SIP/2.0',)):
                sip_msg = line.split(sep=" ")[1] + line.split(sep=" ")[2]
            if line.startswith(('From',)):
                from_hdr = line.split(sep=":")[1]
            if line.startswith(('To',)):
                to_hdr = line.split(sep=":")[1]
            if line.startswith(('Call-ID',)):
                call_id = line.split(sep=":")[1]
            if line.startswith(('Content-Length',)):
                content_length = line.split(sep=":")[1]

            ret_dict.update(
                {time_stamp:(sip_msg, from_hdr, to_hdr, call_id,
                             content_length)})


        except ValueError:
            raise Exception("line is invalid")
        except Exception as e:
            raise e
    print("Ret Dict: ", ret_dict)
    return ret_dict

def main():
    logs = read_logs(log_file)
    print(type(logs))  # should be generator
    logs, logs_copy = tee(logs)
    parse_log_segment(logs)

    print(list(islice(logs_copy, 10)))



if __name__ == '__main__':
    main()
