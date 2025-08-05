import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class SortValuesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, by=None, ascending=True):
        self.by = by
        self.ascending = ascending

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.sort_values(by=self.by, ascending=self.ascending).reset_index(drop=True)
