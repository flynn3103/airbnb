import pandas as pd
from typing import List, Tuple

def get_dataset(csv_path: str):
    data = pd.read_csv(csv_path)
    return data

