import os
import re
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
from data_loader import get_dataloader
from models.dnn_model import MosquitoLSTM

def run_inference(data_dir: str, model_paths: list, output_path: str):
    """
    학습된 5개의 Fold 모델들을 불러와 테스트 데이터에 대한 추론을 수행하고
    각 모델 예측값의 평균(Average Ensemble)을 구하여 제출용 CSV를 생성합니다.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    sample_sub_path = os.path.join(data_dir, 'sample_submission.csv')
    if not os.path.exists(sample_sub_path):
        raise FileNotFoundError(f"Cannot find {sample_sub_path}")
    
    submission_df = pd.read_csv(sample_sub_path)
    
    test_loader = get_dataloader(
        data_dir=data_dir, 
        mode='test', 
        batch_size=32, 
        shuffle=False, 
        num_workers=0
    )
    
    all_fold_preds = []
    
    print(f"Total {len(model_paths)} models found for ensembling.")
    
    for idx, path in enumerate(model_paths):
        print(f"[{idx+1}/{len(model_paths)}] Running inference for model: {os.path.basename(path)}")
        model = MosquitoLSTM(hidden_dim=64, num_layers=2).to(device)
        model.load_state_dict(torch.load(path, map_location=device))
        model.eval()
        
        fold_preds = []
        with torch.no_grad():
            for X_batch, _ in tqdm(test_loader, desc=f"Fold {idx+1} Inference", leave=False):
                X_batch = X_batch.to(device)
                preds = model(X_batch)
                fold_preds.extend(preds.cpu().numpy())
                
        all_fold_preds.append(fold_preds)
        
    # (5, 데이터_수, 3) 차원의 배열을 평균 내어 (데이터_수, 3) 차원으로 변환
    print("Averaging predictions (Ensemble)...")
    final_preds = np.mean(all_fold_preds, axis=0)
    
    submission_df[['x', 'y', 'z']] = final_preds
    submission_df.to_csv(output_path, index=False)
    print(f"Ensemble submission successfully saved to {output_path}")

if __name__ == "__main__":
    data_dir = 'data'
    model_dir = 'models'
    
    if not os.path.exists(model_dir):
        print(f"Error: Model directory '{model_dir}' does not exist.")
    else:
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.pth')]
        if not model_files:
            print(f"Error: No trained model (*.pth) found in {model_dir}")
        else:
            # 가장 최근에 생성된 파일 찾기
            latest_file = max([os.path.join(model_dir, f) for f in model_files], key=os.path.getctime)
            
            # 파일명에서 run_id 추출 (예: lstm_model_abcd123_fold5.pth -> abcd123)
            match = re.search(r'lstm_model_(.+?)_fold', latest_file)
            if match:
                run_id = match.group(1)
                # 동일한 run_id를 가진 모든 5-Fold 모델 파일들을 리스트로 묶음
                target_models = [os.path.join(model_dir, f) for f in model_files if f"lstm_model_{run_id}" in f]
            else:
                # 앙상블이 아닌 예전 단일 모델일 경우를 대비한 안전 장치
                target_models = [latest_file]
            
            output_file = 'submission.csv'
            run_inference(data_dir=data_dir, model_paths=target_models, output_path=output_file)
