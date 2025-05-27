import numpy as np
import librosa

def detect(filepath):
    try:
        y, sr = librosa.load(filepath, sr=None)

        # Compute the cepstrum
        spectrum = np.abs(librosa.stft(y))
        log_spectrum = np.log1p(spectrum)
        cepstrum = np.fft.ifft(log_spectrum, axis=0).real

        # Heuristic: high variance in middle quefrency bins
        quef_bins = cepstrum[30:80, :]
        var_profile = np.var(quef_bins, axis=1)
        avg_var = np.mean(var_profile)

        confidence = min(1.0, avg_var / 5)
        return confidence, f"Cepstral mid-band avg variance: {avg_var:.3f}"

    except Exception as e:
        return 0.0, f"Error in cepstrum analysis: {e}"
