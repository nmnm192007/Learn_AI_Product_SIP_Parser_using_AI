"""
       Read the sip call flow log file and parse the message segments

       @:param
       @:param
       @:return:
"""

from typing import Type, Any, Generator


def read_logs(log_file: str) -> Generator[str, Any, None]:
    """
    Parse the log file
    :param log_file:
    :return:
    """

    try:
        with open(log_file, 'r') as f_obj:
            for line in f_obj.readlines():
                yield line
    except FileNotFoundError:
        raise FileNotFoundError("Log file not found, check LOG_FILE in .env")
    except IOError:
        raise IOError("Log file not found, check LOG_FILE in .env")
    except Exception as e:
        raise e


def parse_log_segment(line: str) -> Dict[str, Any]:
    """
    get the line from log file and parse the message segment
    :param line:
    :return:
    """

    ret_dict: Dict[str, Any] = {}
    time_stamp = msg_dir = sip_msg = from_hdr = to_hdr = call_id = \
        content_length = ""

    if not line:
        return None
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
            {time_stamp:(sip_msg, from_hdr, to_hdr, call_id, content_length)})
        return ret_dict

    except ValueError:
        raise Exception("line is invalid")
    except Exception as e:
        raise e

    return None
