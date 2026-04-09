import os
from pathlib import Path

from dotenv import load_dotenv

from ingestion.pipeline import run_pipeline

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = os.getenv("LOG_FILE")
log_file = BASE_DIR / LOG_FILE


def main():
    msg_v = []
    sessions = run_pipeline(log_file)
    print("run:sessions:", sessions)
    for call_id, msgs in sessions.items():
        print(f"\nCALL_ID:: {call_id}:")
        for msg_k, msg_v in msgs.items():
            print(f"{msg_k}: {msg_v}")


if __name__ == "__main__":
    main()
