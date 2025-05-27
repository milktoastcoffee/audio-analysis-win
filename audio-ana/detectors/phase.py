import numpy as np
import librosa

def detect(filepath):
    try:
        y, sr = librosa.load(filepath, sr=None)
        stft = librosa.stft(y)
        phase = np.angle(stft)

        # Phase delta along time axis
        phase_diff = np.diff(phase, axis=1)
        var_per_bin = np.var(phase_diff, axis=1)

        mean_var = np.mean(var_per_bin)
        confidence = min(1.0, mean_var * 10)  # crude scaling

        if confidence > 0.6:
            return confidence, f"High phase variance detected (avg var: {mean_var:.5f})"
        else:
            return confidence, f"Low/moderate phase variance (avg var: {mean_var:.5f})"

    except Exception as e:
        return 0.0, f"Error in phase detection: {e}"
