"""
This module extends some useful functionality to pandas
"""

import pandas as pd

def null_or_empty(df):
    if isinstance(df, pd.DataFrame):
        return df.isnull() | df.applymap(lambda x: x=='')
    elif isinstance(df, pd.Series):
        return df.isnull() | (df=='')
    else:
        raise ValueError("No implemented!")
