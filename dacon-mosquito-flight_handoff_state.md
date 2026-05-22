# Context Handoff State: Dacon Mosquito Flight Prediction

> **To the New AI Agent:** Read this document immediately to resume context. Do NOT hallucinate past history. We are working entirely in a Local Git + Google Colab runtime environment.

## 1. Completed Tasks (Until V2.0)
- **Data Pipeline:** Created PyTorch `Dataset` & `DataLoader` for 3D time-series coordinates (`src/data_loader.py`).
- **Feature Engineering:** Calculated Velocity and Acceleration physics features (`src/features.py`).
- **Deep Learning Model (V2.0):** 
  - PyTorch LSTM model with `nn.BatchNorm1d` for automatic sequence scaling (`src/models/dnn_model.py`).
  - Inputs expanded from 3(x,y,z) to 5 dimensions (+vel, +accel).
- **Training System:** 
  - 5-Fold Cross Validation & 50 Epochs training loop implemented (`src/train.py`).
  - Weights & Biases (WandB) offline tracking configured.
- **Inference System:** Average Ensemble inference across all 5-Fold models implemented (`src/inference.py`).
- **Documentation:** `README.md` now acts as the Single Source of Truth for the project summary and Model Iteration Log.

## 2. Current State & Pending Issues
- **Status:** WAITING for the User to run the newly pushed V2.0 codebase on Google Colab.
- **Pending Issues:** No current code bugs. The user is executing `!git pull` in Colab, running the 5-fold training, and generating the ensemble `submission.csv`.

## 3. Immediate Next Objectives
1. **Analyze V2.0 Score:** Ask the user for the new Dacon Leaderboard score for V2.0. Compare it against the Baseline score (`0.0278`).
2. **Phase 5 (V3.0) Planning:** Based on the results, proceed to build the LightGBM machine learning ensemble (`src/models/baseline_lgb.py`) or perform Hyperparameter Tuning.
3. **Strict Constraints Reminder:**
   - **No Emojis:** Maintain a strictly professional tone.
   - **Plan Before Action:** Do NOT modify files without explicit "APPROVE" or "승인" from the user.
   - **Language:** Answer directly and concisely in Korean (Code/Variables in English).
