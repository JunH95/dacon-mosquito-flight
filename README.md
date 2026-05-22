# Dacon Mosquito Flight Prediction

## Project Overview
데이콘(Dacon) 모기 비행 예측 대회를 위한 기본 프로젝트 템플릿입니다.

## Directory Structure
- `data/`: 원본 데이터 및 전처리된 데이터 보관 (`.gitignore` 적용)
- `models/`: 학습된 모델 가중치 보관 (`.gitignore` 적용)
- `notebooks/`: EDA 및 실험용 Jupyter Notebooks
- `src/`: 재사용 가능한 소스 코드 (전처리, 학습, 평가 로직)

## Getting Started

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

## 🚀 Model Iteration Log (버전 기록)
> **목적:** 베이스라인부터 최종 모델까지 성능 향상을 위해 적용된 기법과 그 논리적인 이유, 그리고 리더보드 점수 변화를 영구적으로 추적합니다.

| Version | Date | Model Type | Key Changes & Rationale | Public Score | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1.0** | 2026-05-22 | PyTorch LSTM | **[Baseline]** x, y, z 3D 좌표만 단순 입력으로 사용. 파생 변수 부재 및 정규화 미적용으로 인해 인공지능이 유의미한 패턴을 찾지 못함. (학습 10 Epoch) | `0.0278` | 완료 |
| **V2.0** | 2026-05-22 | PyTorch LSTM | **[Feature & Scale Up]**<br>- 1) 속도(Velocity) 및 가속도(Acceleration) 파생변수 주입 (차원 3 ➔ 5)<br>- 2) `nn.BatchNorm1d`를 모델 아키텍처에 삽입하여 GPU 내부에서 실시간 피처 정규화(Scaling) 자동 수행<br>- 3) 5-Fold 교차 검증 앙상블 적용으로 과적합 방지<br>- 4) Epoch 수를 10에서 50으로 대폭 상향 | `Testing` | 진행 중 |

---
*추후 앙상블 기법(LightGBM) 추가 또는 하이퍼파라미터 튜닝 시 이 표에 V3, V4로 계속 기록을 누적합니다.*
