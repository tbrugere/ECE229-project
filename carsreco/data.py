import holoviews as hv
import numpy as np
import pandas as pd

from . import prediction

def get_data() -> pd.DataFrame:
    """Returns the dataframe from the dataset data/preprocessed.csv

    Returns:
        pd.DataFrame: the imported dataframe
    """
    df = pd.read_csv('data/preprocessed.csv', index_col=0, parse_dates=["posting_date"])
    assert isinstance(df, pd.DataFrame)
    return df

#------------------------------------------------------------------------------------
# PREPROCESSING
#------------------------------------------------------------------------------------

def interactive_plots_preprocess(df):
    """Specific preprocessing for interactive plots.

    Choose the data rows with the year after 2000 and price not equal to 0. Drop some irrelevant cols.
    Convert the pd.DataFrame to hv.Dataset

    Args:
        df (pd.DataFrame): Takes in the pd.DataFrame of the dataset

    Returns:
        hv.Dataset: The hv.Dataset of the dataset after preprocessing

    """
    assert isinstance(df, pd.DataFrame), "input should be a pandas DataFrame"

    vdims = ['price']
    kdims = list(df.columns)
    kdims.remove('price')
    edata = hv.Dataset(data=df, kdims=kdims, vdims=vdims)

    return edata

def cats_and_nums(df) -> tuple[list[str], list[str]]:
    """returns categorical / num columns

    Args:
        df: the dataframe

    Returns:
        cats: the list of categorical columns
        nums: the list of numerical columns
    """
    cats = df.select_dtypes(['object', 'category']).columns
    nums = df.select_dtypes(np.number).columns
    return cats, nums

