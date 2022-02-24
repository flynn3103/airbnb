from typing import List, Tuple

import pandas as pd
from sklearn.preprocessing import PowerTransformer


def get_transform(data: List[str]):

    pt = PowerTransformer(method='yeo-johnson')

    numerical_columns = ['accommodates', 'bathrooms', 
                     'bedrooms',
                     'host_listings_count',
                     'maximum_nights', 'minimum_nights',                  
                     'number_of_reviews','price']

    for col in numerical_columns:
        data[col] = data[col].astype('float64')

    data[numerical_columns] = pt.fit_transform(data[numerical_columns])

    return data