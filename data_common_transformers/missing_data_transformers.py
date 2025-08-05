import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class GroupwiseImputer(BaseEstimator, TransformerMixin):    
    def __init__(self, group_col, target_cols, strategy='mean'):
        self.group_col = group_col
        self.target_cols = target_cols
        self.strategy = strategy
        self.fill_values_ = {}
    
    def fit(self, X, y=None):
        X = X.copy()
        
        for col in self.target_cols:
            if self.strategy == 'mean':
                self.fill_values_[col] = X.groupby(self.group_col)[col].mean().to_dict()
            elif self.strategy == 'median':
                self.fill_values_[col] = X.groupby(self.group_col)[col].median().to_dict()
            elif self.strategy == 'mode':
                self.fill_values_[col] = X.groupby(self.group_col)[col].agg(
                    lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan
                ).to_dict()
        
        return self
    
    def transform(self, X):
        X = X.copy()
        
        for col in self.target_cols:
            X[col] = X.apply(
                lambda row: self.fill_values_[col].get(row[self.group_col], row[col]) 
                if pd.isna(row[col]) else row[col], 
                axis=1
            )
        
        return X
    
class SimpleFillnaImputer(BaseEstimator, TransformerMixin):
    def __init__(self, target_cols, strategy='constant', fill_value=0):
        self.target_cols = target_cols
        self.strategy = strategy
        self.fill_value = fill_value
        self.fill_values_ = {}

    def fit(self, X, y=None):
        X = X.copy()
        for col in self.target_cols:
            if self.strategy == 'constant':
                self.fill_values_[col] = self.fill_value
            else:
                raise ValueError("Currently only 'constant' strategy is supported for this use case.")
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.target_cols:
            X[col] = X[col].fillna(self.fill_values_[col])
        return X
