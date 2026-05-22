# Dacon ML & Colab Coding Rules

> Strictly enforced coding standards for PyTorch and LightGBM workflows in the Dacon Mosquito Flight project.

---

## 1. Google Colab Environment Rules
- **Data Paths:** Always use relative paths (`data/train`, `data/train_labels.csv`) in local development, but prepare a Config variable `DATA_DIR` that can be easily switched to `/content/drive/MyDrive/...` when running on Colab.
- **Dependency Management:** Maintain a strict `requirements.txt`. Do not use `!pip install` inside production Python scripts (`src/`).

## 2. PyTorch & LightGBM Standards
- **Data Loader Modularity:** `Dataset` and `DataLoader` classes MUST be isolated in `src/data_loader.py`. Do not mix them with the training loop.
- **Model Modularity:** PyTorch `nn.Module` classes MUST be isolated in `src/models/`.
- **Reproducibility:** Always set random seeds (NumPy, PyTorch, Python random) at the start of any training script.
- **Logging:** All PyTorch training loops must be wrapped with `wandb.log()` for tracking Loss and Evaluation Metrics.

## 3. General Clean Code
- **Language:** English for class/function/variable names. Korean for `# Comments` and `""" Docstrings """`.
- **Type Hinting:** Use strict Python type hints for all function arguments and return types.
