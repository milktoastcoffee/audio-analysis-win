import os
import sys
from datetime import datetime
import numpy as np
import wave

from detectors import lsb, echo, phase, entropy, frequency, cepstrum
from verdict import get_verdict
from logging_utils import log_results, extract_readable_text

def dump_lsb_payload(filepath, output_dir):
    with wave.open(filepath, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)
        bits = samples & 1  # extract LSBs
        bits = bits[:len(bits) - len(bits) % 8]  # pad to full bytes
        bits = bits.astype(np.uint8)  # ensure correct dtype
        bytes_array = np.packbits(bits)

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "lsb_payload.bin"), "wb") as f:
        f.write(bytes_array)


def main(filepath):
    print(f"\nAnalyzing file: {filepath}")

    results = {
        "LSB": lsb.detect(filepath),
        "Echo Hiding": echo.detect(filepath),
        "Phase Shift": phase.detect(filepath),
        "Entropy": entropy.detect(filepath),
        "Frequency Anomaly": frequency.detect(filepath),
        "Cepstral Analysis": cepstrum.detect(filepath),
    }

    final_score, verdict = get_verdict(results)

    print("\n--- Detection Results ---")
    for method, (confidence, notes) in results.items():
        print(f"{method:20s} Confidence = {confidence:.2f} | {notes}")
    print(f"Final Score: {final_score:.2f} | Verdict: {verdict}")

    log_results(filepath, results, final_score, verdict)

    # If LSB confidence is high, extract payload and try to find readable content
    if results['LSB'][0] > 0.9:
        wavname = os.path.splitext(os.path.basename(filepath))[0]
        dump_dir = os.path.join(wavname + " dump")
        os.makedirs(dump_dir, exist_ok=True)

        dump_lsb_payload(filepath, dump_dir)

        # Save a copy of the log in the dump folder
        with open(os.path.join(dump_dir, "results.txt"), "w") as f:
            f.write(f"File: {filepath}\n")
            for method, (confidence, notes) in results.items():
                f.write(f"{method:20s} Confidence = {confidence:.2f} | {notes}\n")
            f.write(f"Final Score: {final_score:.2f} | Verdict: {verdict}\n")

        # Extract readable data
        payload_path = os.path.join(dump_dir, "lsb_payload.bin")
        text, words, runs = extract_readable_text(payload_path)

        print("\n--- Extracted Long Printable Text Runs (length >= 6) ---")
        for run in runs:
            print(run)

        # Save extracted outputs
        with open(os.path.join(dump_dir, "extracted_text.txt"), "w") as f:
            f.write(text)

        with open(os.path.join(dump_dir, "extracted_words.txt"), "w") as f:
            for w in words:
                f.write(w + "\n")

        with open(os.path.join(dump_dir, "extracted_runs.txt"), "w") as f:
            for r in runs:
                f.write(r + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_wav>")
    else:
        main(sys.argv[1])
