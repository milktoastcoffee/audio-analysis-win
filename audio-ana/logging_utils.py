import os
from datetime import datetime
import string
import re

def log_results(filepath, results, final_score, verdict):
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "results.txt")

    with open(log_path, "a") as f:
        f.write(f"\n--- {datetime.now()} ---\n")
        f.write(f"File: {filepath}\n")
        for name, (conf, detail) in results.items():
            f.write(f"{name:20} Confidence = {conf:.2f} | {detail}\n")
        f.write(f"Final Score: {final_score:.2f} | Verdict: {verdict}\n")


def extract_readable_text(payload_path, min_word_length=4, min_run_length=6):
    """
    Reads binary payload and extracts:
    - printable ASCII text,
    - words longer than min_word_length,
    - runs of printable chars longer than min_run_length.
    
    Returns (full_text_string, list_of_words, list_of_runs).
    """
    with open(payload_path, 'rb') as f:
        data = f.read()

    printable_chars = set(string.printable.encode('ascii'))
    filtered_bytes = bytes([b for b in data if b in printable_chars])
    text = filtered_bytes.decode('ascii', errors='ignore')

    # Extract words longer than min_word_length
    words = [w for w in re.findall(r'\b\w+\b', text) if len(w) >= min_word_length]

    # Extract longer runs of printable characters (like sentences or long fragments)
    pattern = rf'[{re.escape(string.printable)}]{{{min_run_length},}}'
    runs = re.findall(pattern, text)

    return text, words, runs
