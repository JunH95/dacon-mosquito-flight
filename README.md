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
