import torch
import torch.nn as nn

class MosquitoLSTM(nn.Module):
    """
    11 스텝의 3D 궤적 데이터를 기반으로 최종 목표 좌표(x, y, z)를 예측하는 LSTM 모델.
    """
    def __init__(self, input_dim: int = 3, hidden_dim: int = 64, num_layers: int = 2, output_dim: int = 3):
        super(MosquitoLSTM, self).__init__()
        # LSTM layer
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        # Fully connected layer for the final 3D coordinate prediction
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x (torch.Tensor): 형태 (batch_size, 11, 4) - timestep_ms, x, y, z
            
        Returns:
            pred (torch.Tensor): 형태 (batch_size, 3) - 예측된 x, y, z
        """
        # 첫 번째 피처(timestep_ms)는 제외하고 x, y, z 좌표만 사용
        coords = x[:, :, 1:] # (batch_size, 11, 3)
        
        # LSTM 연산 수행
        # lstm_out: (batch_size, seq_len, hidden_dim)
        lstm_out, (hn, cn) = self.lstm(coords)
        
        # 시퀀스의 마지막 타임스텝(-1)의 은닉 상태를 추출하여 예측에 사용
        last_out = lstm_out[:, -1, :] # (batch_size, hidden_dim)
        
        # 선형 변환을 통해 최종 3D 좌표 예측
        pred = self.fc(last_out)
        return pred

if __name__ == "__main__":
    # 모델 단위 테스트
    model = MosquitoLSTM()
    dummy_input = torch.randn(8, 11, 4) # batch=8, seq_len=11, features=4
    dummy_output = model(dummy_input)
    print(f"Model output shape: {dummy_output.shape}") # Expected: (8, 3)
