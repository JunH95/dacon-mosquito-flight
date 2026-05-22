import os
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from typing import Tuple, Optional

class MosquitoTrajectoryDataset(Dataset):
    """
    데이콘 모기 비행 궤적 예측을 위한 PyTorch 데이터셋 클래스입니다.
    11개의 타임스텝과 3D 좌표를 포함하는 개별 CSV 파일들을 로드합니다.
    """
    
    def __init__(self, data_dir: str, mode: str = 'train'):
        """
        초기화 함수
        
        Args:
            data_dir (str): 데이터 최상위 디렉토리 (로컬의 경우 'data', Colab의 경우 '/content/drive/MyDrive/...')
            mode (str): 'train' 또는 'test'
        """
        self.data_dir = data_dir
        self.mode = mode
        self.files_dir = os.path.join(data_dir, mode)
        
        if self.mode == 'train':
            labels_path = os.path.join(data_dir, 'train_labels.csv')
            self.labels_df = pd.read_csv(labels_path)
            self.ids = self.labels_df['id'].values
        else:
            # test 모드일 경우 sample_submission.csv를 읽어서 id 목록을 가져옴
            sample_sub_path = os.path.join(data_dir, 'sample_submission.csv')
            self.labels_df = pd.read_csv(sample_sub_path)
            self.ids = self.labels_df['id'].values
            
    def __len__(self) -> int:
        return len(self.ids)
        
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        인덱스에 해당하는 데이터를 불러옴
        
        Returns:
            X (torch.Tensor): 형태 (11, 4) - timestep_ms, x, y, z
            y (torch.Tensor, optional): 형태 (3,) - 타겟 x, y, z (테스트 모드일 경우 None 반환 가능)
        """
        file_id = self.ids[idx]
        file_path = os.path.join(self.files_dir, f"{file_id}.csv")
        
        # CSV 파일 로드 (shape: 11, 4)
        df = pd.read_csv(file_path)
        
        # NumPy 배열로 변환 시 명시적으로 float32로 캐스팅 후 텐서로 변환
        X = torch.tensor(df.values.astype(np.float32), dtype=torch.float32)
        
        if self.mode == 'train':
            # 타겟 (x, y, z) 명시적 형변환
            target = self.labels_df.iloc[idx][['x', 'y', 'z']].values.astype(np.float32)
            y = torch.tensor(target, dtype=torch.float32)
            return X, y
        else:
            # 테스트 환경에서는 레이블이 없음 (더미값 반환)
            y = torch.zeros(3, dtype=torch.float32)
            return X, y

def get_dataloader(data_dir: str, mode: str = 'train', batch_size: int = 32, 
                   shuffle: bool = True, num_workers: int = 4) -> DataLoader:
    """
    DataLoader 생성 함수
    """
    dataset = MosquitoTrajectoryDataset(data_dir=data_dir, mode=mode)
    dataloader = DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=shuffle, 
        num_workers=num_workers,
        pin_memory=True # Colab GPU 학습 시 메모리 효율을 위해 True 설정
    )
    return dataloader

if __name__ == "__main__":
    # 간단한 테스트 로직
    test_dir = "../data" # 스크립트 위치가 src/ 내부일 경우
    if os.path.exists(os.path.join(test_dir, 'train')):
        print("데이터 로더 테스트 중...")
        loader = get_dataloader(test_dir, mode='train', batch_size=4, num_workers=0)
        X_batch, y_batch = next(iter(loader))
        print(f"X_batch shape: {X_batch.shape}") # 예상: (4, 11, 4)
        print(f"y_batch shape: {y_batch.shape}") # 예상: (4, 3)
    else:
        print("데이터 디렉토리를 찾을 수 없어 테스트를 건너뜁니다.")
