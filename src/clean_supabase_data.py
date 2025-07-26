import pandas as pd



def clean_column_names(df):
    df = df.copy()
    df.columns = [
        ('col_' + col if col[0].isdigit() else col).replace(' ', '_')
        for col in df.columns
    ]
    return df


def normalize_columns(df, replace_spaces=True):

    cols = df.columns.str.lower()
    if replace_spaces:
        cols = cols.str.replace(' ', '_')
    df.columns = cols
    return df


