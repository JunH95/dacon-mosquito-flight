import os
import torch
import pandas as pd
from tqdm import tqdm
from data_loader import get_dataloader
from models.dnn_model import MosquitoLSTM

def run_inference(data_dir: str, model_path: str, output_path: str):
    """
    학습된 모델을 불러와 테스트 데이터에 대한 추론을 수행하고 제출용 CSV를 생성합니다.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # sample_submission.csv 로드하여 정답 양식 및 ID 확보
    sample_sub_path = os.path.join(data_dir, 'sample_submission.csv')
    if not os.path.exists(sample_sub_path):
        raise FileNotFoundError(f"Cannot find {sample_sub_path}")
    
    submission_df = pd.read_csv(sample_sub_path)
    
    # 테스트 Dataloader 생성 (순서가 섞이면 안 되므로 shuffle=False 필수)
    test_loader = get_dataloader(
        data_dir=data_dir, 
        mode='test', 
        batch_size=32, 
        shuffle=False, 
        num_workers=0
    )
    
    # 모델 아키텍처 초기화 및 저장된 가중치 불러오기
    # 주의: train.py 에서 사용했던 hidden_dim, num_layers 와 동일하게 설정해야 합니다.
    model = MosquitoLSTM(hidden_dim=64, num_layers=2).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    predictions = []
    
    print("Running inference...")
    with torch.no_grad():
        for X_batch, _ in tqdm(test_loader, desc="Inference"):
            X_batch = X_batch.to(device)
            preds = model(X_batch)
            predictions.extend(preds.cpu().numpy())
            
    # 예측된 3D 좌표를 Dataframe에 반영
    submission_df[['x', 'y', 'z']] = predictions
    
    # 최종 CSV 파일로 저장
    submission_df.to_csv(output_path, index=False)
    print(f"Submission successfully saved to {output_path}")

if __name__ == "__main__":
    # 데이터 폴더와 모델 저장 폴더 (상대 경로)
    data_dir = 'data'
    model_dir = 'models'
    
    # models/ 폴더에서 가장 최근에 생성된 .pth 파일 찾기
    if not os.path.exists(model_dir):
        print(f"Error: Model directory '{model_dir}' does not exist. Please train the model first.")
    else:
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.pth')]
        if not model_files:
            print(f"Error: No trained model (*.pth) found in {model_dir}")
        else:
            # 가장 최신 모델 자동 선택
            latest_model = max([os.path.join(model_dir, f) for f in model_files], key=os.path.getctime)
            print(f"Loading model: {latest_model}")
            
            # 산출물 경로 (루트 디렉토리)
            output_file = 'submission.csv'
            run_inference(data_dir=data_dir, model_path=latest_model, output_path=output_file)
