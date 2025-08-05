import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class DateTimeConverter(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None, format=None):

        self.columns = columns or []
        self.format = format

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.columns:
            if col in X.columns:
                X[col] = pd.to_datetime(X[col], format=self.format, errors='coerce')
        return X
