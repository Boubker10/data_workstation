import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class DateFeatureExtractor(BaseEstimator, TransformerMixin):    
    def __init__(self, date_column='Date', date_format='%d-%m-%Y'):
        self.date_column = date_column
        self.date_format = date_format
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        X[self.date_column] = pd.to_datetime(X[self.date_column], format=self.date_format)
        
        X['month'] = X[self.date_column].dt.month
        X['quarter'] = X[self.date_column].dt.quarter
        X['day_of_week'] = X[self.date_column].dt.dayofweek
        X['week_of_year'] = X[self.date_column].dt.isocalendar().week
        X['is_month_start'] = X[self.date_column].dt.is_month_start.astype(int)
        X['is_month_end'] = X[self.date_column].dt.is_month_end.astype(int)
        
        return X


class SeasonEncoder(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        if 'month' not in X.columns:
            raise ValueError("Column 'month' required")
        
        conditions = [
            X['month'].isin([3, 4, 5]),
            X['month'].isin([6, 7, 8]),
            X['month'].isin([9, 10, 11])
        ]
        choices = ['Spring', 'Summer', 'Autumn']
        X['season'] = np.select(conditions, choices, default='Winter')
        
        return X