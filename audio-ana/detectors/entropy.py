import numpy as np
import librosa

def detect(filepath):
    try:
        y, sr = librosa.load(filepath, sr=None)

        # --- Spectral entropy ---
        S = np.abs(librosa.stft(y))
        S_sum = np.sum(S, axis=0, keepdims=True)
        S_sum[S_sum == 0] = 1e-10  # prevent division by zero
        S_norm = S / S_sum
        spectral_entropy = -np.sum(S_norm * np.log2(S_norm + 1e-10), axis=0)
        avg_entropy = np.mean(spectral_entropy)

        # --- Amplitude entropy ---
        hist, _ = np.histogram(y, bins=256, density=False)
        hist = hist / np.sum(hist)
        hist += 1e-10
        shannon_entropy = -np.sum(hist * np.log2(hist))

        # Combine and score
        entropy_score = (avg_entropy + shannon_entropy) / 2
        confidence = min(1.0, entropy_score / 10)  # normalize for ~0–10 range

        return confidence, f"Spectral Entropy: {avg_entropy:.2f}, Shannon: {shannon_entropy:.2f}"

    except Exception as e:
        return 0.0, f"Error in entropy detection: {e}"
