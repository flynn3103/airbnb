from typing import List

import numpy as np
from sklearn.model_selection import train_test_split

from src.utils.config import TEST_SIZE


def get_train_test_split(X: List[str], y: np.array):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=42
    )
    return X_train, X_test, y_train, y_test