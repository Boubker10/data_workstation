import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class DataFrameMerger(BaseEstimator, TransformerMixin):
    def __init__(self, df_to_merge, on=None, left_on=None, right_on=None, how='left', cols_to_keep=None):
        self.df_to_merge = df_to_merge
        self.on = on
        self.left_on = left_on
        self.right_on = right_on
        self.how = how
        self.cols_to_keep = cols_to_keep  
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.cols_to_keep is None:
            if self.on is not None:
                keys = self.on
            else:
                keys = []
                if self.left_on is not None:
                    keys += self.left_on if isinstance(self.left_on, list) else [self.left_on]
                if self.right_on is not None:
                    keys += self.right_on if isinstance(self.right_on, list) else [self.right_on]
            cols = [col for col in self.df_to_merge.columns if col not in keys]
        else:
            cols = self.cols_to_keep

        if self.on is not None:
            cols_to_merge = list(self.on) + cols
        else:
            right_keys = self.right_on if self.right_on is not None else []
            right_keys = right_keys if isinstance(right_keys, list) else [right_keys]
            cols_to_merge = right_keys + cols

        df_to_merge_subset = self.df_to_merge[cols_to_merge]

        # Effectuer le merge
        X_merged = pd.merge(
            X,
            df_to_merge_subset,
            on=self.on,
            left_on=self.left_on,
            right_on=self.right_on,
            how=self.how,
            suffixes=('', '_drop')
        )

        X_merged = X_merged.loc[:, ~X_merged.columns.str.endswith('_drop')]

        return X_merged
