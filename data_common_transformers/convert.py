import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class ColumnTypeConverter(BaseEstimator, TransformerMixin):

    def __init__(self, columns=None, dtype=None):
        self.columns = columns or []
        self.dtype = dtype

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.columns:
            if col in X.columns and self.dtype is not None:
                X[col] = X[col].astype(self.dtype)
        return X
