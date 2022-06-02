import numpy as np
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

def plot_pie(col, lim = 15, *,  df) -> Figure:
    '''
    Plots the pie chart of the categorical variable col.
    :param col: The name of the categorical column.
    :param lim: The top number of values to group by.
    :return:
    '''

    values = df[col].dropna().value_counts().sort_values(ascending=False)
    topk = min(len(values), lim)
    top_values = values.nlargest(topk)
    if topk > lim: top_values['other'] = values.nsmallest(values.size - topk).sum()
    title = 'Number of cars by %s' % (col.replace('_', ' '))
    fig = px.pie(values, values=top_values.values, names=top_values.index, title=title)
    return fig


def get_groupby_columns(col1: str, col2: str='url', agg: str='count', num_vals: int=1,
                        *, df: pd.DataFrame) -> pd.DataFrame:
    """ This function returns col2 grouped by col1 with aggregation function applied

    Args:
        col1 (str): column to groupby
        col2 (str, optional): column to return. Defaults to 'url'
        agg (str, optional): Aggregation function to be applied. Defaults to 'count'.
        num_vals (int, optional): Top n categories of col1 are returned to make plotting easier. Defaults to 1.
    Returns:
        pd.dataframe: columns specified are returned
    """
    assert col2 in df.columns
    assert col1 in df.columns
    valid_aggregations = {'count', 'mean', 'sum'}
    assert agg in valid_aggregations
    # drop nulls
    df_clean: pd.DataFrame = df.dropna(subset=[col2], axis='index')#type:ignore
    # apply aggregation
    if agg == 'count':
        return df_clean[[col1, col2]].groupby(col1)[col2].count().sort_values(ascending=False).reset_index()
    elif agg == 'mean':
        return df_clean[[col1, col2]].groupby(col1)[col2].mean().sort_values(ascending=False).reset_index()
    elif agg == 'sum':
        return df_clean[[col1, col2]].groupby(col1)[col2].sum().sort_values(ascending=False).reset_index()
    assert False, "Should be unreachable"
    # TODO: add topk handling
