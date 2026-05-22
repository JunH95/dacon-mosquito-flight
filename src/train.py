import os
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import wandb
from tqdm import tqdm
from data_loader import get_dataloader
from models.dnn_model import MosquitoLSTM

def seed_everything(seed: int = 42):
    """
    재현성(Reproducibility)을 위한 랜덤 시드 고정
    """
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def train_model(config: dict = None):
    """
    WandB 연동 PyTorch 학습 루프
    """
    # WandB 초기화
    with wandb.init(project="dacon-mosquito", config=config) as run:
        cfg = wandb.config
        
        # 디바이스 설정
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # 데이터 로더 준비
        train_loader = get_dataloader(
            data_dir=cfg.data_dir, 
            mode='train', 
            batch_size=cfg.batch_size, 
            shuffle=True, 
            num_workers=cfg.num_workers
        )
        
        # 모델 초기화
        model = MosquitoLSTM(
            hidden_dim=cfg.hidden_dim, 
            num_layers=cfg.num_layers
        ).to(device)
        
        # 손실 함수 및 옵티마이저 (기본 MSE 적용)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=cfg.learning_rate)
        
        # 모델 학습 루프
        model.train()
        for epoch in range(cfg.epochs):
            epoch_loss = 0.0
            
            pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{cfg.epochs}")
            for X_batch, y_batch in pbar:
                X_batch = X_batch.to(device)
                y_batch = y_batch.to(device)
                
                optimizer.zero_grad()
                
                preds = model(X_batch)
                loss = criterion(preds, y_batch)
                
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
                pbar.set_postfix({'loss': loss.item()})
                
            avg_loss = epoch_loss / len(train_loader)
            
            # WandB 로그 기록
            wandb.log({
                "epoch": epoch + 1, 
                "train_loss": avg_loss
            })
            
        # 체크포인트 저장
        save_dir = os.path.join(cfg.data_dir, '../models')
        os.makedirs(save_dir, exist_ok=True)
        model_path = os.path.join(save_dir, f'lstm_model_{run.id}.pth')
        torch.save(model.state_dict(), model_path)
        print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    seed_everything(42)
    
    # 학습 하이퍼파라미터 설정 (Colab vs Local)
    # Colab에서 실행 시 data_dir을 '/content/drive/MyDrive/...' 형태로 덮어쓸 수 있습니다.
    default_config = {
        'data_dir': '../data',
        'epochs': 10,
        'batch_size': 32,
        'learning_rate': 1e-3,
        'hidden_dim': 64,
        'num_layers': 2,
        'num_workers': 0 # Colab 환경에서는 GPU 효율을 위해 2~4 권장
    }
    
    # 로컬 테스트용 환경변수 (실제 훈련이 아니므로 로깅 생략)
    # os.environ["WANDB_MODE"] = "offline"
    
    # 학습 실행을 원할 경우 주석 해제 (로컬엔 데이터가 없을 수 있으므로 Colab 권장)
    # train_model(config=default_config)
