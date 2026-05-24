import numpy as np
import pandas as pd

def calculate_velocity_accel_jerk(trajectory: np.ndarray) -> tuple:
    """
    11개의 타임스텝에 대한 3D 궤적(x, y, z)을 바탕으로 속도, 가속도, Jerk(가속도 변화량)를 계산합니다.
    
    Args:
        trajectory (np.ndarray): (11, 4) 배열. 첫 번째 열은 timestep_ms, 나머지 3열은 (x,y,z).
        
    Returns:
        velocity (np.ndarray): (10,) 배열. 각 구간별 유클리디안 속도 스칼라값.
        acceleration (np.ndarray): (9,) 배열. 각 구간별 가속도.
        jerk (np.ndarray): (8,) 배열. 각 구간별 가속도의 변화량(Jerk).
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
    
    # Jerk = 가속도 변화량 / 시간
    da = np.diff(acceleration)
    dt_jerk = dt_accel[1:] # 8개의 구간
    jerk = da / dt_jerk
    
    return velocity, acceleration, jerk

def extract_features_lgb(trajectory: np.ndarray) -> np.ndarray:
    """
    LightGBM 베이스라인 모델 학습을 위해 시계열 데이터를 1D Feature Vector로 변환합니다.
    통계적 파생 변수(평균 속도, 최대 가속도 등) 및 Jerk 피처를 생성합니다.
    """
    coords = trajectory[:, 1:]
    
    # 1. 원본 3D 좌표 평탄화 (11스텝 * 3좌표 = 33 features)
    flat_coords = coords.flatten()
    
    # 2. 물리적 피처 계산
    vel, accel, jerk = calculate_velocity_accel_jerk(trajectory)
    
    # 3. 주요 통계 변수 (Rolling & Global Statistics)
    # 최근 3스텝(가장 중요한 막바지 움직임)
    recent_vel = vel[-3:] if len(vel) >= 3 else vel
    recent_accel = accel[-3:] if len(accel) >= 3 else accel
    
    stats = np.array([
        # 전체 통계
        np.mean(vel), np.max(vel), np.min(vel), np.std(vel),
        np.mean(accel), np.max(accel), np.min(accel), np.std(accel),
        np.mean(jerk), np.max(jerk), np.min(jerk), np.std(jerk),
        
        # 최근 3스텝 통계 (방향 전환 포착용)
        np.mean(recent_vel), np.std(recent_vel),
        np.mean(recent_accel), np.std(recent_accel),
        
        # Start-to-End 직선 거리
        np.linalg.norm(coords[-1] - coords[0])
    ])
    
    # 전체 Feature Vector 결합
    # 33 + 10 + 9 + 8 + 17 = 77차원
    features = np.concatenate([flat_coords, vel, accel, jerk, stats])
    
    return np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)

def extract_features_lstm(trajectory: np.ndarray) -> np.ndarray:
    """
    LSTM 모델 학습을 위해 시계열 데이터를 (11, 5) Feature Sequence로 변환합니다.
    (기존 코드 유지)
    """
    coords = trajectory[:, 1:] # (11, 3)
    # 호환성을 위해 앞의 2개 반환값만 사용
    vel, accel, _ = calculate_velocity_accel_jerk(trajectory) 
    
    vel_padded = np.insert(vel, 0, vel[0]) # (11,)
    accel_padded = np.insert(accel, 0, [accel[0], accel[0]]) # (11,)
    
    features = np.column_stack((coords, vel_padded, accel_padded))
    return np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)

if __name__ == "__main__":
    dummy_trajectory = np.zeros((11, 4))
    dummy_trajectory[:, 0] = np.linspace(-400, 0, 11)
    dummy_trajectory[:, 1:] = np.random.rand(11, 3)
    
    feats = extract_features_lgb(dummy_trajectory)
    print(f"Extracted feature vector shape: {feats.shape}") # Expected: (77,)
