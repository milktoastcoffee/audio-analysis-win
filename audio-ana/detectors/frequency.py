import numpy as np
import librosa
import scipy.stats

def detect(filepath):
    try:
        y, sr = librosa.load(filepath, sr=None)

        # --- FFT Analysis ---
        fft_spectrum = np.fft.fft(y)
        magnitude = np.abs(fft_spectrum)
        norm_magnitude = magnitude / np.sum(magnitude)

        # Check for unexpected spikes
        zscore = scipy.stats.zscore(norm_magnitude[:len(norm_magnitude)//2])
        spike_count = np.sum(np.abs(zscore) > 4)

        # --- Spectral flatness ---
        S = np.abs(librosa.stft(y))
        flatness = librosa.feature.spectral_flatness(S=S)
        avg_flatness = np.mean(flatness)

        # Heuristics:
        # - too flat = white noise
        # - too spiky = possible embedding
        confidence = min(1.0, (spike_count / 20 + avg_flatness * 5))

        notes = f"{spike_count} FFT spikes | Avg flatness: {avg_flatness:.3f}"
        return confidence, notes

    except Exception as e:
        return 0.0, f"Error in frequency domain analysis: {e}"
