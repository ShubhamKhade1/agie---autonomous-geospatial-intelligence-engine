import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, List, Optional
from sklearn.preprocessing import MinMaxScaler

class LSTMPredictor(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, output_dim: int):
        super(LSTMPredictor, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # LSTM Layer
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        
        # Fully Connected Layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Initial hidden and cell states
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        
        # Forward pass through LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

class TemporalEngine:
    def __init__(self, input_dim: int = 3, hidden_dim: int = 64, num_layers: int = 2):
        """
        :param input_dim: Number of parallel sensors (e.g., SST, CHL, AIS)
        """
        self.model = LSTMPredictor(input_dim, hidden_dim, num_layers, input_dim)
        self.scaler = MinMaxScaler()
        self.input_dim = input_dim
        self.is_trained = False

    def prepare_data(self, data: np.ndarray, window_size: int = 30) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Convert raw series into sliding window chunks (Batch, Window, Features).
        """
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(len(scaled_data) - window_size):
            X.append(scaled_data[i : i + window_size])
            y.append(scaled_data[i + window_size])
            
        return torch.tensor(np.array(X), dtype=torch.float32), torch.tensor(np.array(y), dtype=torch.float32)

    def train_baseline(self, data: np.ndarray, epochs: int = 20):
        """
        Fast 'Cold Start' training on historical baseline data.
        """
        X, y = self.prepare_data(data)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.MSELoss()

        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            output = self.model(X)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
            
        self.is_trained = True

    def calculate_reconstruction_error(self, recent_history: np.ndarray, current_val: np.ndarray) -> float:
        """
        Calculate the anomaly score based on prediction deviation.
        :param recent_history: Matrix of (Window x Features)
        :param current_val: Vector of (Features)
        :return: Normalized error (0-1)
        """
        if not self.is_trained:
            return 0.5 # Default uncertainty

        self.model.eval()
        with torch.no_grad():
            # Scale and reshape
            history_scaled = self.scaler.transform(recent_history)
            current_scaled = self.scaler.transform(current_val.reshape(1, -1))
            
            x_input = torch.tensor(history_scaled, dtype=torch.float32).unsqueeze(0)
            prediction = self.model(x_input).numpy()
            
            # MSE between prediction and actual
            error = np.mean((prediction - current_scaled) ** 2)
            
            # Normalize error into 0-1 range (capped at 5 sigma-ish)
            score = np.clip(error * 10, 0, 1)
            return score

if __name__ == "__main__":
    # Test Logic
    engine = TemporalEngine(input_dim=2)
    mock_history = np.random.normal(0, 1, (100, 2))
    engine.train_baseline(mock_history)
    
    # Normal point
    test_val = np.random.normal(0, 1, (1, 2))
    print(f"Normal Error: {engine.calculate_reconstruction_error(mock_history[-30:], test_val)}")
    
    # Anomalous point (Spike)
    anom_val = np.array([[10.0, 10.0]])
    print(f"Anomalous Error: {engine.calculate_reconstruction_error(mock_history[-30:], anom_val)}")
