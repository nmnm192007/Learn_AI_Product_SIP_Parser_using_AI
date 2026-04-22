import os
from pathlib import Path

from dotenv import load_dotenv

from ingestion.pipeline import run_pipeline

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = os.getenv("LOG_FILE")
log_file = BASE_DIR / LOG_FILE


def main():

    chunks = run_pipeline(log_file)


if __name__ == "__main__":
    main()
