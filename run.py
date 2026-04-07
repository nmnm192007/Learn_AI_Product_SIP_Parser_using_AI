
from pathlib import Path
import os
from dotenv import load_dotenv

from ingestion.pipeline import run_pipeline

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = os.getenv("LOG_FILE")
log_file = BASE_DIR / LOG_FILE


def main():
   sessions = run_pipeline(log_file)
   print(sessions)
   for call_id, msgs in sessions.items():
       print(f"\nCALL_ID:: {call_id}:")
       for msg in msgs:
           print(msg["sip_msg"], msg["direction"])


if __name__ == "__main__":
    main()