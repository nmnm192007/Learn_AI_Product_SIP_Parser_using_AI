import os
from pathlib import Path

from dotenv import load_dotenv

from ingestion.pipeline import run_pipeline

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = os.getenv("LOG_FILE")
log_file = BASE_DIR / LOG_FILE


def main():
    query_text = (
        # "explain which all were the successful calls, also explain when call failed"
        """
            Identify:
                1. Successful calls
                2. Failed calls
                3. Error codes
                4. Termination reason
                5. Call duration
        """
    )

    prompt_result = run_pipeline(log_file, query_text)
    print("\n Answer :: \n")
    print(prompt_result)


if __name__ == "__main__":
    main()
