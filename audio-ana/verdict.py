def get_verdict(results):
    """
    Takes a dict of {name: (confidence, detail)} and returns an overall score and verdict.
    High-confidence results override averaging.
    """
    weights = {
        'LSB': 1.2,
        'Echo Hiding': 0.8,
        'Phase Shift': 1.0,
        'Entropy': 0.6,
        'Frequency Anomaly': 1.0,
        'Cepstral Analysis': 0.4
    }

    # PRIORITY OVERRIDE: Any strong detector forces verdict
    critical_hits = []
    for method in ['LSB', 'Phase Shift', 'Frequency Anomaly']:
        if results[method][0] >= 0.95:
            critical_hits.append(method)

    if critical_hits:
        final_score = 1.0
        verdict = f"Definite Stego (via: {', '.join(critical_hits)})"
        return final_score, verdict

    # Weighted average if no critical hits
    total_weight = sum(weights.values())
    weighted_score = sum(conf * weights.get(name, 1.0) for name, (conf, _) in results.items())
    final_score = weighted_score / total_weight

    if final_score >= 0.85:
        verdict = "Likely Stego"
    elif final_score >= 0.5:
        verdict = "Possibly Stego"
    else:
        verdict = "Likely Clean"

    return final_score, verdict
