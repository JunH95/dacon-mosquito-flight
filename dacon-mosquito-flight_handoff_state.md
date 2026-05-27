# Handoff State: Dacon Mosquito Flight Prediction

## 1. 현재 프로젝트 상태 (Current Status)
- **대회 목표:** 모기 비행 궤적 예측 (R-Hit@1cm 최대화, 현재 1등 스코어 0.7022)
- **현재 최신 아키텍처:** V4.0 (LightGBM 앙상블)
- **최고 달성 점수:** **0.1794** (기존 딥러닝 베이스라인 0.0278 대비 6.5배 상승)
- **실행 환경:** Google Colab (`notebooks/colab_runner.ipynb` 중심 원클릭 런처 사용)

## 2. 완료된 핵심 작업 (Completed Milestones)
- **자체 평가 파이프라인 완성 (`src/evaluate.py`)**: 공식 평가 산식(R-Hit) 내장 및 오차 원인 분석을 위한 마크다운 리포트 자동 생성.
- **물리적 피처 엔지니어링 (`src/features.py`)**: 3D 절대 좌표를 넘어 속도, 가속도, **가속도 변화량(Jerk)** 및 최근 3스텝 이동 분산 등 통계 피처 추출 로직 구축 (총 77차원).
- **타겟 차분 예측 기법 (Delta Prediction)**: 예측 대상을 '절대 좌표'에서 '마지막 위치(11번째) 기준 상대적 변동량(Delta)'으로 치환하여 성능 폭등 견인.
- **독립 머신러닝 파이프라인 구축 (`src/train_lgb.py`, `src/inference_lgb.py`)**: PyTorch 환경과 격리된 LightGBM 학습, 5-Fold 교차 검증, Delta 복원 앙상블 스크립트 작성.

## 3. 현재 문제점 및 한계 (Pending Issues / Bottlenecks)
- 단일 트리 모델(LightGBM)과 기본 설정된 임의의 하이퍼파라미터(`max_depth=7` 등)에 의존하고 있어 모델 포텐셜의 한계 도달.
- 최상위권(0.70점대) 도약을 위해서는 아직 약 4배가량의 점수 상승이 요구됨.

## 4. 새로운 세션에서의 다음 목표 (Next Objectives for V5.0)
> **[새로운 AI 에이전트를 위한 지시사항] 이 파일을 읽은 즉시 아래의 V5.0 업그레이드를 기획하고 실행하십시오.**
1. **Optuna 하이퍼파라미터 자동 최적화**: 트리 구조 성능을 극대화하기 위해 베이지안 최적화(Optuna)를 적용하여 베스트 파라미터 자동 탐색 뼈대 구축.
2. **트리 삼대장 앙상블 확장**: LightGBM 코드를 응용하여 XGBoost, CatBoost 학습 파이프라인을 나란히 구축하고, 3개 모델의 예측값을 최종 평균 내는 하드코어 앙상블 구현.
3. **고급 파생 변수(비선형 물리) 추가**: 단순 직선 가속도 외에 비행 궤적의 3차원 방향성(각도 Yaw/Pitch, 곡률 등)을 나타내는 수식(Trigonometry) 피처 추가.
4. **(선택) LSTM 부활 실험**: Delta Prediction 아이디어를 기존 `src/models/dnn_model.py`에 적용하여 버려졌던 딥러닝 성능 복구 시도.
