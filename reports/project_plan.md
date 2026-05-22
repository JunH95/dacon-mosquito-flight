# Dacon 모기 비행 궤적 예측 프로젝트 통합 계획서 (Tech PM & Lead)

해당 문서는 "모기 비행 궤적 예측 AI 경진대회"에 참여하기 위한 **PM(제품 요구사항 및 마일스톤 설계)**과 **Tech Lead(시스템 아키텍처 및 기술 스택 선정)**의 통합된 실행 계획서(PRD & Architecture)입니다.

---

## 1. 🎯 아이디어 검증 및 목표 정의 (PM)
- **핵심 문제:** 과거 모기의 비행 궤적(400ms 전 ~ 0ms까지의 3D 좌표, `x`, `y`, `z`)을 기반으로 미래 특정 시점의 좌표(`x`, `y`, `z`)를 예측하는 회귀(Regression) 문제.
- **경쟁력 (1등 목표):** 단순한 통계적 시계열 모델뿐만 아니라 딥러닝 기반의 시퀀스 모델(RNN, Transformer)을 앙상블하여 높은 Hit Rate 성능을 달성.
- **제약 조건:** 로컬 GPU가 없으므로 무거운 모델 훈련 시 구글 코랩(Google Colab) 환경을 메인 런타임으로 활용. 로컬 환경은 데이터 탐색 및 코드 작성용으로만 사용.

## 2. 👥 사용자 플로우 (User Story)
- **데이터 분석가(본인):** 
  - 코랩 환경에서 구글 드라이브(또는 Dacon API)를 통해 제공된 `train/`, `test/` 데이터를 효율적으로 로드할 수 있다.
  - 모기의 비행 패턴을 분석(가속도, 방향 전환 등 파생 변수 생성)하고 EDA를 수행한다.
  - 설계된 딥러닝/머신러닝 파이프라인으로 모델을 학습시키고 `sample_submission.csv` 형식에 맞춰 추론 결과를 산출한다.

## 3. 🛠 기술 스택 추천 및 선정 (Tech Lead)
로컬 리소스의 한계를 극복하고 빠르고 안정적인 모델링을 위해 아래와 같은 스택을 권장합니다.
- **환경 및 인프라:** Google Colab (학습 환경), GitHub (버전 관리)
- **주요 언어:** Python 3.10+
- **데이터 전처리:** `Pandas`, `NumPy`, `Scikit-learn`
- **모델링 (Model):** 
  - *LightGBM/XGBoost*: 시계열 데이터를 롤링 피처(평균, 분산, 차분 등)로 변환한 후 학습하는 베이스라인 모델용.
  - *PyTorch*: LSTM, GRU 또는 시계열 Transformer(Time-Series Transformer)를 통한 고성능 예측 모델용.
- **실험 관리:** `Weights & Biases (WandB)` (하이퍼파라미터 튜닝 및 손실 함수 트래킹)

## 4. 🗄 데이터 모델링 및 처리 파이프라인
- **입력 데이터 구조:** 
  - `TRAIN_XXXXX.csv`: 각 모기의 비행 단위. (11, 4) 배열 (`timestep_ms`, `x`, `y`, `z`).
  - 시계열 데이터를 하나의 PyTorch `Dataset`으로 변환하여 배치 단위로 로드.
- **파생 변수 (Feature Engineering):**
  - **속도 (Velocity):** 각 축별 시간당 변화량
  - **가속도 (Acceleration):** 속도의 시간당 변화량
  - **방향성 및 스칼라 거리:** 이동 방향 각도 변화 및 이동 거리

## 5. 📁 폴더 및 시스템 블루프린트 (Architecture)
프로젝트 내 코랩 및 로컬 연동을 위한 최적 구조입니다.

```text
dacon-mosquito-flight/
├── data/                    # 데이터 폴더
│   ├── train/               # 입력 시계열 (11 timesteps)
│   ├── test/
│   ├── train_labels.csv     # 타겟 (x, y, z)
│   └── sample_submission.csv
├── notebooks/
│   └── 01_EDA_and_Baseline.ipynb # 코랩 연동용 주피터 노트북
├── src/                     # 핵심 로직 (재사용 모듈)
│   ├── __init__.py
│   ├── data_loader.py       # PyTorch Dataset 및 Dataloader 정의
│   ├── features.py          # 속도/가속도 등 파생변수 생성기
│   ├── models/
│   │   ├── baseline_lgb.py  # LightGBM 학습 코드
│   │   └── dnn_model.py     # PyTorch 시퀀스 모델
│   └── train.py             # 학습 및 검증 루프 (WandB 연동)
├── requirements.txt         # 패키지 목록
└── README.md
```

## 6. 🚀 단계별 실행 계획 (Milestones)

- **Phase 1 (준비):** 구글 코랩 연동을 위한 데이터 파이프라인 구성 및 PyTorch `Dataset`(`src/data_loader.py`) 스크립트 작성.
- **Phase 2 (특성 공학):** 시계열 데이터를 평탄화(Flatten) 및 파생변수화 하는 로직(`src/features.py`) 구현.
- **Phase 3 (학습 로직 구현):** 베이스라인 LightGBM 및 PyTorch 기반 딥러닝 모델(`src/models/dnn_model.py`) 아키텍처 작성.
- **Phase 4 (최적화 및 추론):** 하이퍼파라미터 튜닝 및 최종 제출물(Submission) 생성 파이프라인 작성.

---

> [!IMPORTANT]
> **User Review Required**
> 본 프로젝트 설계서는 로컬 GPU 부재를 고려하여 **Colab 환경(학습)과 로컬(스크립트 작성) 투트랙 접근**을 상정하고 있습니다. 
> 제안된 폴더 구조 및 모델링 전략(가속도 등 파생 변수를 활용한 앙상블 전략)에 동의하시나요? 
> 승인(APPROVE)해 주시면 바로 `Phase 1` 단계인 데이터 로더 스크립트(`src/data_loader.py`)부터 작성을 시작하겠습니다.
