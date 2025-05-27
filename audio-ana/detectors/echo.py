import numpy as np
import librosa
import scipy.signal

def detect(filepath):
    try:
        y, sr = librosa.load(filepath, sr=None)

        # Autocorrelation
        autocorr = scipy.signal.correlate(y, y, mode='full')
        mid = len(autocorr) // 2
        autocorr = autocorr[mid:]  # keep positive lags

        # Find peaks in autocorrelation (echoes)
        peaks, _ = scipy.signal.find_peaks(autocorr, height=np.max(autocorr)*0.3, distance=sr//100)

        # Heuristic: multiple regularly spaced strong peaks → possible echo hiding
        spacing = np.diff(peaks)
        if len(spacing) < 2:
            return 0.1, "Few/no echo peaks detected"

        std_dev = np.std(spacing)
        confidence = max(0.0, 1.0 - std_dev / np.mean(spacing))

        return confidence, f"{len(peaks)} echo peaks detected (std spacing: {std_dev:.2f})"

    except Exception as e:
        return 0.0, f"Error in echo detection: {e}"
