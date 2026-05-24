import os
import joblib
import numpy as np
import pandas as pd
from features import extract_features_lgb

def load_lgb_test_data(data_dir: str):
    sample_sub_path = os.path.join(data_dir, 'sample_submission.csv')
    sub_df = pd.read_csv(sample_sub_path)
    ids = sub_df['id'].values
    
    test_dir = os.path.join(data_dir, 'test')
    
    X_list = []
    print("Extracting features from test data...")
    for file_id in ids:
        file_path = os.path.join(test_dir, f"{file_id}.csv")
        df = pd.read_csv(file_path)
        feats = extract_features_lgb(df.values)
        X_list.append(feats)
        
    X = np.array(X_list)
    last_coords = X[:, 30:33]
    
    return X, last_coords, sub_df

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    model_dir = os.path.join(base_dir, 'models')
    result_dir = os.path.join(base_dir, 'result')
    os.makedirs(result_dir, exist_ok=True)
    
    X_test, last_coords, sub_df = load_lgb_test_data(data_dir)
    
    # 5-Fold 모델 앙상블 추론
    delta_preds = []
    
    for fold in range(1, 6):
        model_path = os.path.join(model_dir, f'lgbm_fold_{fold}.pkl')
        if not os.path.exists(model_path):
            print(f"Warning: {model_path} not found. Skipping...")
            continue
            
        print(f"Loading {model_path} and predicting...")
        model = joblib.load(model_path)
        fold_pred = model.predict(X_test)
        delta_preds.append(fold_pred)
        
    if not delta_preds:
        raise FileNotFoundError("학습된 LightGBM 모델을 찾을 수 없습니다. train_lgb.py를 먼저 실행하세요.")
        
    # 5개 모델의 예측값 평균 산출
    avg_delta_pred = np.mean(delta_preds, axis=0)
    
    # Delta(변화량) 값을 11번째 절대 위치에 더하여 최종 좌표 복원
    final_abs_pred = last_coords + avg_delta_pred
    
    # 제출 파일 업데이트
    sub_df['x'] = final_abs_pred[:, 0]
    sub_df['y'] = final_abs_pred[:, 1]
    sub_df['z'] = final_abs_pred[:, 2]
    
    # 파일 저장
    output_path = os.path.join(result_dir, 'submission_v4_lgb.csv')
    sub_df.to_csv(output_path, index=False)
    print(f"\n✅ Inference completed. Submission file saved to: {output_path}")
