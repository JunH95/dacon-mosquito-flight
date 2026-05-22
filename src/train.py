import os
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import wandb
from tqdm import tqdm
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader, Subset
from data_loader import MosquitoTrajectoryDataset
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
    5-Fold Cross Validation 및 50 Epoch 적용 PyTorch 학습 루프
    """
    with wandb.init(project="dacon-mosquito", config=config) as run:
        cfg = wandb.config
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # 1. 전체 데이터셋 객체 로드
        dataset = MosquitoTrajectoryDataset(data_dir=cfg.data_dir, mode='train')
        
        # 2. 5-Fold 교차 검증 객체 생성
        kfold = KFold(n_splits=cfg.n_splits, shuffle=True, random_state=42)
        
        save_dir = os.path.join(cfg.data_dir, '../models')
        os.makedirs(save_dir, exist_ok=True)
        
        fold_results = []
        
        # 3. 각 Fold별로 훈련 반복
        for fold, (train_idx, val_idx) in enumerate(kfold.split(dataset)):
            print(f"\n====================================")
            print(f"       Fold {fold+1} / {cfg.n_splits} Start!")
            print(f"====================================")
            
            # Sub 데이터셋 분리
            train_sub = Subset(dataset, train_idx)
            val_sub = Subset(dataset, val_idx)
            
            # DataLoader 생성
            train_loader = DataLoader(train_sub, batch_size=cfg.batch_size, shuffle=True, num_workers=cfg.num_workers)
            val_loader = DataLoader(val_sub, batch_size=cfg.batch_size, shuffle=False, num_workers=cfg.num_workers)
            
            # 매 Fold마다 모델과 옵티마이저를 새로 초기화
            model = MosquitoLSTM(
                hidden_dim=cfg.hidden_dim, 
                num_layers=cfg.num_layers
            ).to(device)
            
            criterion = nn.MSELoss()
            optimizer = optim.Adam(model.parameters(), lr=cfg.learning_rate)
            
            best_val_loss = float('inf')
            model_path = os.path.join(save_dir, f'lstm_model_{run.id}_fold{fold+1}.pth')
            
            # Epoch 반복
            for epoch in range(cfg.epochs):
                model.train()
                epoch_loss = 0.0
                
                # Training Loop
                pbar = tqdm(train_loader, desc=f"[Fold {fold+1}] Epoch {epoch+1}/{cfg.epochs}")
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
                    
                avg_train_loss = epoch_loss / len(train_loader)
                
                # Validation Loop
                model.eval()
                val_loss = 0.0
                with torch.no_grad():
                    for X_val, y_val in val_loader:
                        X_val = X_val.to(device)
                        y_val = y_val.to(device)
                        val_preds = model(X_val)
                        v_loss = criterion(val_preds, y_val)
                        val_loss += v_loss.item()
                        
                avg_val_loss = val_loss / len(val_loader)
                
                # 로그 기록
                wandb.log({
                    f"fold_{fold+1}_train_loss": avg_train_loss,
                    f"fold_{fold+1}_val_loss": avg_val_loss,
                    "epoch": epoch + 1
                })
                
                # 가장 성능이 좋은(Validation Loss가 가장 낮은) 시점의 가중치만 저장
                if avg_val_loss < best_val_loss:
                    best_val_loss = avg_val_loss
                    torch.save(model.state_dict(), model_path)
            
            print(f"\n=> Fold {fold+1} Best Validation Loss: {best_val_loss:.5f}")
            fold_results.append(best_val_loss)
            
        print(f"\n✅ All 5 Folds Training Completed!")
        print(f"Average Validation Loss across all folds: {np.mean(fold_results):.5f}")

if __name__ == "__main__":
    seed_everything(42)
    
    default_config = {
        'data_dir': 'data',
        'epochs': 50,         # 10회에서 50회로 대폭 증가
        'batch_size': 32,
        'learning_rate': 1e-3,
        'hidden_dim': 64,
        'num_layers': 2,
        'num_workers': 0,
        'n_splits': 5         # 5-Fold Cross Validation 적용
    }
    
    train_model(config=default_config)
