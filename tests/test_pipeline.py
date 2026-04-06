
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
LOG_FILE = os.getenv("LOG_FILE")

# Step 1 : Get path of log_file
log_file = BASE_DIR / LOG_FILE


from ingestion.parser import read_logs, parse_log_segment
from ingestion.normalizer import Normalizer

# Step 2: Read logs
log_gen = read_logs(log_file)

# Step 3: Parse Logs
parsed_gen = parse_log_segment(log_gen)

# Step 4: Initialize normalizer
normalizer = Normalizer()

# Step 5: Process ONE message
# first_msg = next(parsed_gen)

for msg in parsed_gen:
	print("\n--- PARSED MESSAGE ---")
	print(msg)

	cleaned_msg = normalizer.normalize(msg)

	print("\n  --- NORMALIZED MESSAGE --- ")
	print(cleaned_msg)
	print("\n-----------------------------------")

