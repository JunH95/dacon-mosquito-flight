# Dacon Mosquito Flight Prediction

## 1. Project Overview
이 프로젝트는 과거에 모기가 날아간 궤적을 보고, 다음 순간 모기가 어디에 있을지 예측하는 AI를 만드는 것이 목표입니다.
모기는 파리나 벌과 달리 비행 패턴이 매우 불규칙하고 톡톡 튀는 특징이 있습니다. 카메라나 LiDAR 센서로 포착한 모기의 찰나의 움직임을 바탕으로 미래 위치(Hit Rate)를 정확히 맞추는 것이 핵심입니다.

## 2. Data Structure
대회에서 제공된 데이터(TRAIN_XXXXX.csv)는 모기 1마리의 과거 0.4초 동안의 비행 기록입니다.
- 시간(Timestep): 0.04초(40ms) 간격으로 측정되어, 총 11번의 사진이 찍혀 있습니다. (-400ms ~ 0ms)
- 공간 좌표(X, Y, Z): 사진이 찍힐 때마다 모기가 위치한 3차원 공간의 좌표값입니다.
- 목표(Label): 이 11개의 궤적 기록을 보고, 다음 순간(미래)의 최종 (x, y, z) 좌표를 예측해야 합니다.

## 3. Modeling Pipeline & Rationale
우리는 단순히 좌표의 숫자만 AI에게 던져주지 않고, 모기의 '운동 역학'을 AI가 이해하기 쉽게 가공(Feature Engineering)하는 기법을 선택했습니다.

### 파생 변수 생성: 속도(Velocity)와 가속도(Acceleration) 추출
- 이유: 단순히 (x, y, z) 위치만으로는 모기가 지금 빠르게 날아가는 중인지, 갑자기 방향을 트는 중인지 알기 어렵습니다. 
- 적용: 물리 법칙에 따라 (거리 / 시간) 공식을 적용해 매 순간의 이동 속도를 구하고, (속도 변화량 / 시간)을 통해 가속도를 계산했습니다. EDA 결과, 모기는 순간적인 가속 패턴을 보인다는 사실을 확인하고 이를 학습 변수에 추가했습니다.

### 모델링 기법: LSTM 딥러닝 (Deep Learning)
- 이유: LSTM(Long Short-Term Memory)은 시간의 흐름(순서)을 기억하는 데 특화된 인공지능입니다.
- 적용: 1번부터 11번까지의 궤적 순서를 그대로 모델에 입력합니다. AI가 모기의 동선 흐름을 암기하다가 마지막 11번째 위치에서 다음 위치를 직관적으로 예측하도록 시스템을 설계했습니다.

## 4. Directory Structure
- data/: 원본 데이터 및 전처리된 데이터 보관 (.gitignore 적용)
- models/: 학습된 모델 가중치 보관 (.gitignore 적용)
- notebooks/: EDA 및 실험용 Jupyter Notebooks
- src/: 재사용 가능한 소스 코드 (전처리, 학습, 평가 로직)

## 5. Getting Started
```bash
# 가상환경 생성 및 활성화
conda create -n dacon-mosquito python=3.10
conda activate dacon-mosquito

# 패키지 설치
pip install -r requirements.txt
```

## 6. Model Iteration Log
> 목적: 베이스라인부터 최종 모델까지 성능 향상을 위해 적용된 기법과 그 논리적인 이유, 그리고 리더보드 점수 변화를 영구적으로 추적합니다.

| Version | Date | Model Type | Key Changes & Rationale | Public Score | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1.0** | 2026-05-22 | PyTorch LSTM | **[Baseline]** x, y, z 3D 좌표만 단순 입력으로 사용. 파생 변수 부재 및 정규화 미적용으로 인해 인공지능이 유의미한 패턴을 찾지 못함. (학습 10 Epoch) | 0.0278 | 완료 |
| **V2.0** | 2026-05-22 | PyTorch LSTM | **[Feature & Scale Up]**<br>- 1) 속도 및 가속도 파생변수 주입 (차원 3 -> 5)<br>- 2) nn.BatchNorm1d를 삽입하여 GPU 내부에서 실시간 피처 정규화(Scaling) 수행<br>- 3) 5-Fold 교차 검증 앙상블 적용으로 과적합 방지<br>- 4) Epoch 수를 10에서 50으로 상향 | Testing | 완료 |

---
*추후 앙상블 기법(LightGBM) 추가 또는 하이퍼파라미터 튜닝 시 이 표에 V3, V4로 계속 기록을 누적합니다.*
