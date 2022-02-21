from typing import List, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def get_standarization(data: List[str]) ->Tuple[StandardScaler, np.array]:

    X = data.drop('price', axis=1)
    y = data.price
    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=list(X.columns))
    return X, y