from sklearn.pipeline import make_pipeline
from src.connect import fetch_feature, run_query
from data_common_transformers.merge_data import DataFrameMerger
from data_common_transformers.missing_data_transformers import SimpleFillnaImputer

query = """
SELECT m."Store", m."Date"
FROM walmart AS m
"""
portfolio = run_query(query)

base_df = fetch_feature("date_feature", portfolio=portfolio)

pipe = make_pipeline(
    DataFrameMerger(
        df_to_merge=fetch_feature("interaction_features", portfolio=portfolio),
        on=["store", "date"], how="left"
    ),
    DataFrameMerger(
        df_to_merge=fetch_feature("growth_features", portfolio=portfolio),
        on=["store", "date"], how="left"
    ),
    DataFrameMerger(
        df_to_merge=fetch_feature("rolling_features", portfolio=portfolio),
        on=["store", "date"], how="left"
    ),
    SimpleFillnaImputer(
        target_cols=[
            "weekly_sales_rolling_std_2", 
            "weekly_sales_rolling_std_4", 
            "weekly_sales_pct_change", 
            "weekly_sales_diff"
        ],
        strategy='constant',
        fill_value=0
    )
)

def fit_transform(X=None):
    if X is None:
        X = base_df
    return pipe.fit_transform(X)
