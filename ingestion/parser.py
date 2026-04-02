"""
       Read the sip call flow log file and parse the message segments

       @:param
       @:param
       @:return:
"""

from typing import Type, Any, Generator


def read_logs(log_file:str)-> Generator[str, Any, None]:
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




def parse_log_segment(line:str):
    """

    :param line:
    :return:
    """
    ret_dict = {}
    if not line:
        return None
    line = line.strip()
    if line.strip().startswith(' '):
        return None
    try:
       if line.startswith('['):
           time_stamp = line.split(sep=" ")[0]
           msg_dir = line.split(sep=" ")[1]
           ret_dict[time_stamp] = time_stamp
           ret_dict[msg_dir] = msg_dir



    except ValueError:
        raise Exception("line is invalid")
        
    return None


    

