import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL
from typing import List, Dict, Any, Optional
from src.engine.reasoning.temporal_nn import TemporalEngine
import os

class AnomalyScorer:
    def __init__(self, w_recency=0.2, w_magnitude=0.4, w_trajectory=0.2, w_neural=0.2):
        """
        :param w_recency: Weight for data freshness
        :param w_magnitude: Weight for deviation from baseline (STL)
        :param w_trajectory: Weight for historical trajectory (persistence)
        :param w_neural: Weight for neural reconstruction error (LSTM)
        """
        self.w_recency = w_recency
        self.w_magnitude = w_magnitude
        self.w_trajectory = w_trajectory
        self.w_neural = w_neural
        
        # Neural Engine for Pattern Analysis
        self.neural_engine = TemporalEngine(input_dim=1) # Scalable per sensor

    def calculate_magnitude(self, signal: pd.Series, period: int = 365) -> pd.Series:
        """
        Calculate the deviation from the seasonal baseline using STL.
        :param signal: Pandas series of normalized values
        :param period: Seasonal period (365 for daily year)
        :return: Residual (Magnitude of anomaly)
        """
        # Decompose the signal into Trend, Seasonal, and Residuals
        res = STL(signal, period=period).fit()
        # Return the absolute residual normalized by the standard deviation
        residuals = res.resid
        magnitude = np.abs(residuals) / np.std(residuals)
        return magnitude

    def calculate_trajectory(self, magnitude: pd.Series, window: int = 7) -> pd.Series:
        """
        Calculate the rolling persistence of the anomaly.
        :param magnitude: Magnitude series
        :param window: Time window for trajectory calculation
        :return: Trajectory score
        """
        # A persistence score based on the rolling mean of magnitudes
        trajectory = magnitude.rolling(window=window).mean()
        return trajectory

    def compute_hybrid_score(
        self, 
        signal_dict: Dict[str, pd.Series], 
        recency_val: float, 
        period: int = 365
    ) -> float:
        """
        Final 1-100 Hybrid Anomaly Score (Step 3).
        Combines Statistical (STL) and Neural (LSTM) components.
        """
        total_score = 0
        sensor_weights = {"SST": 1.0, "CHL": 0.8, "SAR": 1.2, "AIS": 1.5} # Domain-specific confidence
        
        for name, series in signal_dict.items():
            # 1. Statistical Magnitude (STL)
            magnitudes = self.calculate_magnitude(series, period)
            current_magnitude = magnitudes.iloc[-1]
            m_norm = np.clip(current_magnitude / 3.0, 0, 1)

            # 2. Neural Pattern Error (LSTM)
            # Train on the fly for 'Cold Start' with higher epochs for pattern learning
            if not self.neural_engine.is_trained:
                self.neural_engine.train_baseline(series.values.reshape(-1, 1), epochs=50)
            
            # Use last 30 window for prediction
            # We scale the reconstruction error to ensure pattern breaks are visible
            n_error_raw = self.neural_engine.calculate_reconstruction_error(
                series.values[-31:-1].reshape(-1, 1), # x_input
                series.values[-1].reshape(-1, 1)      # y_actual
            )
            n_error = np.clip(n_error_raw * 5.0, 0, 1) # Amplify for 1-100 scale
            
            # 3. Temporal Trajectory
            trajectories = self.calculate_trajectory(magnitudes)
            t_norm = np.clip(trajectories.iloc[-1] / 2.0, 0, 1)

            # Sensor-specific Weighted Component
            sensor_priority = (self.w_recency * recency_val) + \
                             (self.w_magnitude * m_norm) + \
                             (self.w_neural * n_error) + \
                             (self.w_trajectory * t_norm)
            
            total_score += sensor_priority * sensor_weights.get(name, 1.0)

        # Normalize across all sensors and scale to 100
        final_score = (total_score / len(signal_dict)) * 100
        return np.clip(final_score, 0, 100)

if __name__ == "__main__":
    # Test example with mock signal
    scorer = AnomalyScorer()
    # mock_signal = pd.Series(np.random.normal(0, 1, 1000))
    # score = scorer.compute_priority_score(mock_signal, 0.95)
    # print(f"Final Anomaly Score: {score}")
