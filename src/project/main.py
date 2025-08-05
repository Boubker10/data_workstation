import pandas as pd
from sklearn.pipeline import make_pipeline
from src.connect import fetch_feature, run_query
from data_common_transformers.merge_data import DataFrameMerger
from data_common_transformers.missing_data_transformers import SimpleFillnaImputer
from data_common_transformers.convert import ColumnTypeConverter
from data_common_transformers.sortvalues import SortValuesTransformer
from data_common_transformers.todatetime import DateTimeConverter

def convert_date_columns(dfs, date_col='date', date_format='%d-%m-%Y'):
    for df in dfs:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], format=date_format)
    return dfs

query = """
SELECT m."Store", m."Date"
FROM walmart AS m
"""
portfolio = run_query(query)

df_date_feature = fetch_feature("date_feature", portfolio=portfolio)
df_interaction = fetch_feature("interaction_features", portfolio=portfolio)
df_growth = fetch_feature("growth_features", portfolio=portfolio)
df_rolling = fetch_feature("rolling_features", portfolio=portfolio)

[df_date_feature, df_interaction, df_growth, df_rolling] = convert_date_columns(
    [df_date_feature, df_interaction, df_growth, df_rolling],
    date_col='date',
    date_format='%d-%m-%Y'
)

pipe = make_pipeline(
    DateTimeConverter(columns=['date'], format='%d-%m-%Y'),
    DataFrameMerger(
        df_to_merge=df_interaction,
        on=["store", "date"], how="left"
    ),
    DataFrameMerger(
        df_to_merge=df_growth,
        on=["store", "date"], how="left"
    ),
    DataFrameMerger(
        df_to_merge=df_rolling,
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
    ),
    ColumnTypeConverter(columns=["season"], dtype='category'),
    ColumnTypeConverter(columns=["month","day_of_week","week_of_year","quarter","Holiday_Flag"], dtype="float64"),
    SortValuesTransformer(by=["store","date"], ascending=True)
)

base_df = df_date_feature  

def fit_transform(X=None):
    if X is None:
        X = base_df
    return pipe.fit_transform(X)
