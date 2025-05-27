import numpy as np
import wave

def detect(filepath):
    try:
        with wave.open(filepath, 'rb') as wav:
            frames = wav.readframes(wav.getnframes())
            samples = np.frombuffer(frames, dtype=np.int16)

        # Extract LSBs
        lsb_bits = samples & 1
        unique, counts = np.unique(lsb_bits, return_counts=True)
        bit_distribution = dict(zip(unique, counts))

        # Heuristic: if nearly 50/50, it's suspicious
        ratio = abs(counts[0] - counts[1]) / sum(counts)
        confidence = 1.0 - ratio  # closer to 0.5 = higher confidence

        return confidence, f"Bit distribution: {bit_distribution}"

    except Exception as e:
        return 0.0, f"Error in LSB detection: {e}"
