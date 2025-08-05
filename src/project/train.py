import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def train_and_evaluate(
    data, 
    features,
    store_id = 1,
    n_estimators=150,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    objective='reg:squarederror',
    enable_categorical=True
):
    df_store1 = data[data['store'] == store_id].copy()
    df_store1 = df_store1.dropna()

    test_start = '2012-09-01'
    test_end = '2012-10-30'

    sept_oct_2012_data = df_store1[(df_store1['date'] >= test_start) & (df_store1['date'] <= test_end)]
    data_wo_sept_oct2012 = df_store1[(df_store1['date'] < test_start) | (df_store1['date'] > test_end)]

    X = data_wo_sept_oct2012[features]
    y = data_wo_sept_oct2012['Weekly_Sales']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = XGBRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state,
        objective=objective,
        enable_categorical=enable_categorical
    )

    model.fit(X_train, y_train)

    return model 

