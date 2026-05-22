import os
import torch
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import KFold
from data_loader import MosquitoTrajectoryDataset
from models.dnn_model import MosquitoLSTM

def r_hit_array(pred: np.ndarray, true: np.ndarray, threshold: float = 0.01) -> np.ndarray:
    distances = np.linalg.norm(pred - true, axis=-1)
    return (distances <= threshold).astype(float)

def generate_error_report(model_path: str, data_dir: str, output_path: str, fold: int = 1):
    """
    학습된 모델의 검증 성능을 상세히 분석하여 마크다운 보고서로 저장합니다.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 데이터 로드 (분석을 위해 Fold 1의 Validation 데이터만 사용)
    dataset = MosquitoTrajectoryDataset(data_dir=data_dir, mode='train')
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    splits = list(kfold.split(dataset))
    _, val_idx = splits[fold - 1]
    
    val_sub = Subset(dataset, val_idx)
    val_loader = DataLoader(val_sub, batch_size=32, shuffle=False, num_workers=0)
    
    # 모델 로드
    model = MosquitoLSTM(hidden_dim=64, num_layers=2).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    all_preds = []
    all_trues = []
    all_speeds = []
    
    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            X_batch_dev = X_batch.to(device)
            preds = model(X_batch_dev).cpu().numpy()
            trues = y_batch.numpy()
            
            # 입력 데이터에서 마지막 타임스텝의 속도 피처(인덱스 3)를 추출하여 난이도 구분용으로 사용
            # X_batch shape: (batch, 11, 5) - [x, y, z, velocity, acc]
            last_speed = X_batch[:, -1, 3].numpy()
            
            all_preds.extend(preds)
            all_trues.extend(trues)
            all_speeds.extend(last_speed)
            
    all_preds = np.array(all_preds)
    all_trues = np.array(all_trues)
    all_speeds = np.array(all_speeds)
    
    # 1. 전체 R-Hit 분석
    hits = r_hit_array(all_preds, all_trues)
    overall_r_hit = np.mean(hits)
    
    # 2. 축별 절대 오차 (MAE) 분석
    abs_errors = np.abs(all_preds - all_trues)
    mean_errors = np.mean(abs_errors, axis=0) # [x, y, z]
    
    # 3. 편향(Bias) 분석: 예측값 - 실제값 (음수면 Under-shooting, 양수면 Over-shooting)
    biases = np.mean(all_preds - all_trues, axis=0)
    
    # 4. 속도 구간별 성능 분석 (느림 vs 빠름)
    median_speed = np.median(all_speeds)
    slow_mask = all_speeds <= median_speed
    fast_mask = all_speeds > median_speed
    
    slow_r_hit = np.mean(hits[slow_mask]) if np.sum(slow_mask) > 0 else 0
    fast_r_hit = np.mean(hits[fast_mask]) if np.sum(fast_mask) > 0 else 0
    
    # 마크다운 보고서 작성
    report = f"# Model Error Analysis Report\n\n"
    report += f"- **Analyzed Model**: `{os.path.basename(model_path)}`\n"
    report += f"- **Validation Fold**: {fold}\n"
    report += f"- **Overall R-Hit@1cm**: **{overall_r_hit:.4f}**\n\n"
    
    report += f"## 1. 축별 오차(MAE) 분석\n"
    report += f"모델이 어느 축에서 가장 헤매고 있는지 파악합니다. 수치가 클수록 오차가 큽니다.\n"
    report += f"- **X축 오차**: {mean_errors[0]:.4f} m\n"
    report += f"- **Y축 오차**: {mean_errors[1]:.4f} m\n"
    report += f"- **Z축 오차**: {mean_errors[2]:.4f} m\n\n"
    
    report += f"## 2. 방향성 편향(Bias) 진단\n"
    report += f"양수(+)는 실제보다 과대예측(Over-shooting), 음수(-)는 과소예측(Under-shooting)을 의미합니다.\n"
    report += f"- **X축 편향**: {biases[0]:.4f}\n"
    report += f"- **Y축 편향**: {biases[1]:.4f}\n"
    report += f"- **Z축 편향**: {biases[2]:.4f}\n\n"
    
    report += f"## 3. 모기 비행 속도별 성능 차이\n"
    report += f"마지막 타임스텝의 속도를 기준으로 그룹을 나누어 평가합니다.\n"
    report += f"- **저속 비행 구간 R-Hit**: {slow_r_hit:.4f}\n"
    report += f"- **고속 비행 구간 R-Hit**: {fast_r_hit:.4f}\n\n"
    
    report += f"## 💡 Actionable Insights (다음 단계 제안)\n"
    if overall_r_hit < 0.1:
        report += f"- **심각한 성능 저하**: 전반적인 예측이 빗나가고 있습니다. 타겟 스케일링 부재로 인한 Mean Collapse 가능성이 높으므로 LightGBM 전환이 시급합니다.\n"
    if fast_r_hit < slow_r_hit * 0.5:
        report += f"- **고속 구간 취약**: 모기가 빠르게 움직일 때 예측이 무너집니다. 물리적 가속도 피처를 더 강하게 주입하거나 비선형 모델(트리) 앙상블이 필요합니다.\n"
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Report successfully saved to {output_path}")

if __name__ == "__main__":
    # 가장 최근에 학습된 1-Fold 모델을 찾아서 분석
    model_dir = '../models'
    data_dir = '../data'
    report_dir = '../reports'
    
    if os.path.exists(model_dir):
        model_files = [f for f in os.listdir(model_dir) if f.endswith('fold1.pth')]
        if model_files:
            latest_model = max([os.path.join(model_dir, f) for f in model_files], key=os.path.getctime)
            output_report = os.path.join(report_dir, 'latest_model_evaluation.md')
            generate_error_report(latest_model, data_dir, output_report, fold=1)
        else:
            print("fold1.pth 모델을 찾을 수 없습니다. 학습(train.py)을 먼저 진행하세요.")
    else:
        print("models 폴더가 존재하지 않습니다.")
