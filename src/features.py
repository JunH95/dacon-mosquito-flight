import numpy as np
import pandas as pd
import torch

def calculate_velocity_accel(trajectory: np.ndarray) -> tuple:
    """
    11개의 타임스텝에 대한 3D 궤적(x, y, z)을 바탕으로 속도와 가속도를 계산합니다.
    
    Args:
        trajectory (np.ndarray): (11, 4) 배열. 첫 번째 열은 timestep_ms, 나머지 3열은 (x,y,z).
        
    Returns:
        velocity (np.ndarray): (10,) 배열. 각 구간별 유클리디안 속도 스칼라값.
        acceleration (np.ndarray): (9,) 배열. 각 구간별 가속도.
    """
    coords = trajectory[:, 1:] 
    time = trajectory[:, 0]
    
    # 시간 간격 계산 (기본 40ms)
    dt = np.diff(time)
    dt = np.where(dt == 0, 1e-6, dt) # 0으로 나누기 방지
    
    # 유클리디안 거리 변화량
    dp = np.diff(coords, axis=0)
    dist = np.linalg.norm(dp, axis=1)
    
    # 속도 = 거리 / 시간
    velocity = dist / dt
    
    # 가속도 = 속도 변화량 / 시간
    dv = np.diff(velocity)
    dt_accel = dt[1:] # 9개의 구간
    acceleration = dv / dt_accel
    
    return velocity, acceleration

def extract_features_lgb(trajectory: np.ndarray) -> np.ndarray:
    """
    LightGBM 베이스라인 모델 학습을 위해 시계열 데이터를 1D Feature Vector로 변환합니다.
    통계적 파생 변수(평균 속도, 최대 가속도 등)를 생성합니다.
    """
    coords = trajectory[:, 1:]
    
    # 1. 원본 3D 좌표 평탄화 (11스텝 * 3좌표 = 33 features)
    flat_coords = coords.flatten()
    
    # 2. 속도 및 가속도 배열
    vel, accel = calculate_velocity_accel(trajectory)
    
    # 3. 주요 통계 변수 추출
    stats = np.array([
        np.mean(vel), np.max(vel), np.min(vel), np.std(vel),
        np.mean(accel), np.max(accel), np.min(accel), np.std(accel),
        np.linalg.norm(coords[-1] - coords[0]) # Start-to-End 직선 거리
    ])
    
    # 전체 Feature Vector 결합
    # (33) + (10) + (9) + (9) = 총 61차원의 입력 피처
    features = np.concatenate([flat_coords, vel, accel, stats])
    
    return features

if __name__ == "__main__":
    # 테스트용 더미 궤적 데이터 (11, 4)
    dummy_trajectory = np.zeros((11, 4))
    dummy_trajectory[:, 0] = np.linspace(-400, 0, 11) # timestep
    dummy_trajectory[:, 1:] = np.random.rand(11, 3)   # x, y, z 랜덤
    
    feats = extract_features_lgb(dummy_trajectory)
    print(f"Extracted feature vector shape: {feats.shape}") # Expected: (61,)
