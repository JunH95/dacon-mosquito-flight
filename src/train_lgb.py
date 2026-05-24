import os
import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import KFold
from features import extract_features_lgb

def r_hit_array(pred: np.ndarray, true: np.ndarray, threshold: float = 0.01) -> np.ndarray:
    distances = np.linalg.norm(pred - true, axis=-1)
    return (distances <= threshold).astype(float)

def load_lgb_data(data_dir: str):
    labels_df = pd.read_csv(os.path.join(data_dir, 'train_labels.csv'))
    ids = labels_df['id'].values
    targets_abs = labels_df[['x', 'y', 'z']].values
    
    train_dir = os.path.join(data_dir, 'train')
    
    X_list = []
    for file_id in ids:
        file_path = os.path.join(train_dir, f"{file_id}.csv")
        df = pd.read_csv(file_path)
        feats = extract_features_lgb(df.values)
        X_list.append(feats)
        
    X = np.array(X_list)
    
    # 11번째 타임스텝의 절대 좌표 추출 (features 배열의 30~32번 인덱스)
    last_coords = X[:, 30:33]
    
    # 모델 타겟: 최종 절대 좌표(targets_abs)가 아닌 "마지막 위치로부터의 이동량(Delta)"
    y_delta = targets_abs - last_coords
    
    return X, y_delta, targets_abs

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    print("Loading data and extracting features...")
    X, y_delta, targets_abs = load_lgb_data(data_dir)
    print(f"X shape: {X.shape}, y_delta shape: {y_delta.shape}")
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    overall_r_hits = []
    
    for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
        print(f"\n--- Fold {fold+1} ---")
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y_delta[train_idx], y_delta[val_idx]
        val_targets_abs = val_targets_abs = targets_abs[val_idx]
        val_last_coords = X_val[:, 30:33]
        
        # 모델 정의
        # n_estimators, max_depth 등은 추후 튜닝 가능. 기본 베이스라인 설정.
        lgbm = LGBMRegressor(n_estimators=200, max_depth=7, learning_rate=0.05, random_state=42, verbose=-1)
        model = MultiOutputRegressor(lgbm)
        
        # 학습
        model.fit(X_train, y_train)
        
        # 추론 (Delta 예측)
        val_delta_pred = model.predict(X_val)
        
        # Delta를 절대 좌표로 복원
        val_abs_pred = val_last_coords + val_delta_pred
        
        # R-Hit 산식으로 평가
        hits = r_hit_array(val_abs_pred, val_targets_abs)
        r_hit_score = np.mean(hits)
        overall_r_hits.append(r_hit_score)
        
        print(f"Fold {fold+1} R-Hit@1cm: {r_hit_score:.4f}")
        
        # 모델 저장
        model_path = os.path.join(model_dir, f'lgbm_fold_{fold+1}.pkl')
        joblib.dump(model, model_path)
        print(f"Saved model to {model_path}")
        
    print(f"\n✅ 5-Fold Average R-Hit@1cm: {np.mean(overall_r_hits):.4f}")
