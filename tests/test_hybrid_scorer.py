import pandas as pd
import numpy as np
from src.engine.reasoning.anomaly_scorer import AnomalyScorer

def test_hybrid_logic():
    scorer = AnomalyScorer()
    
    # Generate 100 days of normal data (Seasonal sine wave + noise)
    time = np.linspace(0, 100, 100)
    normal_series = pd.Series(10 * np.sin(2 * np.pi * time / 10) + np.random.normal(0, 1, 100))
    
    # Case 1: Normal Point
    signals_normal = {"SST": normal_series}
    score_normal = scorer.compute_hybrid_score(signals_normal, 1.0)
    print(f"Normal Data Score: {score_normal:.2f}")
    
    # Case 2: Statistical Anomaly (Large Magnitude Spike)
    anom_magnitude = normal_series.copy()
    anom_magnitude.iloc[-1] += 50.0 # Huge spike
    score_mag = scorer.compute_hybrid_score({"SST": anom_magnitude}, 1.0)
    print(f"Magnitude Anomaly Score: {score_mag:.2f}")
    
    # Case 3: Neural Anomaly (Pattern Break - not necessarily high magnitude)
    # We break the sine wave pattern but keep the value within normal range
    anom_pattern = normal_series.copy()
    anom_pattern.iloc[-1] = 0.0 # Flat line instead of peak
    score_pattern = scorer.compute_hybrid_score({"SST": anom_pattern}, 1.0)
    print(f"Pattern Anomaly Score: {score_pattern:.2f}")

    assert score_mag > score_normal
    assert score_pattern > score_normal
    print("\u2705 Hybrid Logic Verified!")

if __name__ == "__main__":
    test_hybrid_logic()
