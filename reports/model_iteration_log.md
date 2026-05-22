# 🧬 Dacon Mosquito Flight: Model Iteration Log

> **목적:** 베이스라인부터 최종 모델까지 성능 향상을 위해 적용된 기법과 그 논리적인 이유, 그리고 리더보드 점수 변화를 영구적으로 추적합니다.

| Version | Date | Model Type | Key Changes & Rationale | Public Score | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1.0** | 2026-05-22 | PyTorch LSTM | **[Baseline]** x, y, z 3D 좌표만 단순 입력으로 사용. 파생 변수 부재 및 정규화 미적용으로 인해 인공지능이 유의미한 패턴을 찾지 못함. (학습 10 Epoch) | `0.0278` | 완료 |
| **V2.0** | 2026-05-22 | PyTorch LSTM | **[Feature & Scale Up]**<br>- 1) 속도(Velocity) 및 가속도(Acceleration) 파생변수 주입 (차원 3 ➔ 5)<br>- 2) `nn.BatchNorm1d`를 모델 아키텍처에 삽입하여 GPU 내부에서 실시간 피처 정규화(Scaling) 자동 수행<br>- 3) 5-Fold 교차 검증 앙상블 적용으로 과적합 방지<br>- 4) Epoch 수를 10에서 50으로 대폭 상향 | `Testing` | 진행 중 |

---
*추후 앙상블 기법(LightGBM) 추가 또는 하이퍼파라미터 튜닝 시 이 문서 하단에 V3, V4로 계속 기록을 누적합니다.*
