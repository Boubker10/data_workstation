from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

class GroupwiseScaler(BaseEstimator, TransformerMixin):   
    def __init__(self, group_col, target_cols, scaler_type='standard'):
        self.group_col = group_col
        self.target_cols = target_cols
        self.scaler_type = scaler_type
        self.scalers_ = {}
    
    def fit(self, X, y=None):
        X = X.copy()
        
        for group in X[self.group_col].unique():
            group_data = X[X[self.group_col] == group][self.target_cols]
            
            if self.scaler_type == 'standard':
                scaler = StandardScaler()
            elif self.scaler_type == 'minmax':
                scaler = MinMaxScaler()
            else:
                raise ValueError("scaler_type must be 'standard' or 'minmax'")
            
            self.scalers_[group] = scaler.fit(group_data)
        
        return self
    
    def transform(self, X):
        X = X.copy()
        
        for group in X[self.group_col].unique():
            mask = X[self.group_col] == group
            if group in self.scalers_:
                X.loc[mask, self.target_cols] = self.scalers_[group].transform(
                    X.loc[mask, self.target_cols]
                )
        
        return X