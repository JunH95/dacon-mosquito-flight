# Validation & Error Analysis Pipeline Walkthrough

데이콘 하루 제출 제한을 극복하고, 모델 예측의 취약점을 자체적으로 분석하기 위한 **'로컬 진단 및 평가 파이프라인'** 구축 작업을 성공적으로 완료했습니다.

## 주요 변경 사항 요약

### 1. `src/train.py` 고도화 (R-Hit Metric 내장)
- **대회 공식 지표 적용**: 기존 MSE Loss뿐만 아니라, Dacon 공식 산식인 `R-Hit@1cm` 점수를 매 Epoch마다 계산하는 `r_hit()` 함수를 추가했습니다.
- **WandB 로깅 동기화**: `train_r_hit`, `val_r_hit` 지표를 Weights & Biases 로그에 추가하여, 시각적인 학습 곡선을 통해 과적합 여부를 즉각 파악할 수 있게 되었습니다.
- **체크포인트(Checkpoint) 기준 변경**: Validation Loss가 가장 낮은 모델 대신, **Validation R-Hit 점수가 가장 높은 모델**을 최종 저장하도록 `best_val_r_hit` 추적 로직으로 교체했습니다.

### 2. `src/evaluate.py` 신규 생성 (자체 오답 노트 시스템)
단순 점수 측정을 넘어, 모델이 구체적으로 어떤 물리적/방향적 오류를 범하고 있는지 분석하는 독립된 진단 스크립트를 구현했습니다.
- **축별 절대 오차(MAE) 분석**: X, Y, Z 방향별로 모델이 얼마나 벗어났는지 진단.
- **방향성 편향(Bias) 분석**: 모델이 모기의 이동을 보수적으로 예측(Under-shooting)하는지 진단.
- **속도 구간별 R-Hit 측정**: 입력된 마지막 타임스텝의 속도를 기준으로 '저속'과 '고속'을 분리하여, 모기가 갑자기 튈 때 성능이 무너지는지 확인.
- **리포트 자동 생성**: 분석된 지표를 바탕으로 `reports/latest_model_evaluation.md` 경로에 상세 진단 보고서를 자동 저장하는 기능을 탑재했습니다.

## 🚀 다음 사용자 액션 (Action Item)

이 변경 사항은 현재 로컬 PC에 저장되어 있습니다. Google Colab 환경에서 다음 단계를 수행하여 파이프라인을 검증해 주세요.

1. **Git Commit & Push**: 수정한 `train.py`와 `evaluate.py`를 GitHub 리포지토리에 푸시합니다.
2. **Colab에서 모델 재학습**: 
   ```bash
   !git pull origin main
   !python src/train.py
   ```
3. **평가 및 리포트 확인**:
   ```bash
   !python src/evaluate.py
   ```
   이후 `reports/` 폴더에 생성된 **평가 보고서(.md)**를 읽고, V3.0 (LightGBM 등) 개발 방향을 결정합니다.
