"""
This module extends some useful functionality to pandas
"""

import pandas as pd

def null_or_empty(df):
    return df.isnull() | df.applymap(lambda x: x=='')
