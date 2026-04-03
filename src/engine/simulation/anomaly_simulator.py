import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict

def generate_dark_vessel_anomaly(points: int = 100) -> Dict[str, pd.Series]:
    """
    Simulate a multi-sensor anomaly:
    - Normal baseline for 90% of the series.
    - Anomaly trigger in the final 10% of the series.
    """
    time = np.linspace(0, points, points)
    
    # 1. SST (Thermal): Seasonal Baseline + Spike
    sst_baseline = 25 + 2 * np.sin(2 * np.pi * time / 50) # Normal seasonal curve
    sst_noise = np.random.normal(0, 0.2, points)
    sst_spike = np.zeros(points)
    sst_spike[-10:] = np.linspace(0, 5, 10) # 5 degree spike at the end
    sst_series = pd.Series(sst_baseline + sst_noise + sst_spike)
    
    # 2. AIS (Transponder): Signal Active (1) -> Lost (0)
    ais_signal = np.ones(points)
    ais_signal[-15:] = 0 # Signal lost 15 points ago
    ais_series = pd.Series(ais_signal)
    
    # 3. SAR (Metallic / Slick): Zero (0) -> Detection (1)
    sar_detection = np.zeros(points)
    sar_detection[-10:] = 1 # Detection matches SST spike
    sar_series = pd.Series(sar_detection)
    
    return {
        "SST": sst_series,
        "AIS": ais_series,
        "SAR": sar_series
    }

if __name__ == "__main__":
    # Test generation
    data = generate_dark_vessel_anomaly()
    print("Injected Anomaly Signals Generated.")
    print(f"Final SST: {data['SST'].iloc[-1]:.2f}")
    print(f"Final AIS: {data['AIS'].iloc[-1]}")
    print(f"Final SAR: {data['SAR'].iloc[-1]}")
