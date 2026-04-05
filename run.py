from ingestion.parser import read_logs, parse_log_segment
from itertools import tee, islice
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = os.getenv("LOG_FILE")
log_file = BASE_DIR / LOG_FILE


def main():
    logs = read_logs(log_file)
    logs, logs_copy = tee(logs)

    print(list(islice(logs_copy, 10)))
    print("\n PARSED OUTPUT :: \n")

    for parsed in parse_log_segment(logs):
        print(parsed)


if __name__ == "__main__":
    main()