import numpy as np
import pandas as pd

import holoviews as hv
import plotly.express as px


def price_trendency_plot(edata, kdim="state"):
    """Holoview curve plot combined with errorbar plot of average price trendency.

    Aggregate the data given the k-dimension and generate the errorbar plot and curve plot.

    Args:
        edata (hv.Dataset): The hv.Dataset of the dataset
        kdim (str): The key-dimension

    Returns:
        hv.core.overlay.Overlay: The holoview curve plot combined with errorbar plot

    """
    assert isinstance(kdim, str), "Please input your interested key dimension as string"

    agg = edata.aggregate(kdim, function=np.mean, spreadfn=np.std).sort()
    if len(agg) >= 20:
        width = 800
    elif 10 <= len(agg) < 20:
        width = 600
    else:
        width = 400

    if kdim == "year":
        edata = edata[(edata['year']>=2000) & (edata['year']<=2021)]
    agg = edata.aggregate(kdim, function=np.mean, spreadfn=np.std).sort()
    errorbars = hv.ErrorBars(agg,vdims=['price', 'price_std']).iloc[::1]
    overlay =  (hv.Curve(agg) * errorbars).redim.range(price=(0, None)).opts(width=width, xrotation=45, title='Average Price Fluctuation by %s' % kdim)

    return overlay


def count_plot(df, kdim="manufacturer", lim=15):
    """Holoview count bars plot of the k-dimension.

    Groupby the k-dimension, get the counts and sort them.
    Generate the Holoviews bars plot using pandas.hvplot.

    Args:
        df (pd.DataFrame): The DataFrame of the dataset
        kdim (str): The key-dimension
        lim (int): The limitation number of bars

    Returns:
        hv.element.chart.Bars: The holoview bars plot.

    """
    assert isinstance(kdim, str), "Please input your interested key dimension as string"

    # key_df = df.groupby([kdim]).size().sort_values(ascending=True).rename('count').reset_index()[:lim]
    values = df[kdim].dropna().value_counts().sort_values(ascending=False)
    topk = min(len(values), lim)
    top_values = values.nlargest(topk)
    if len(values) > lim: top_values['other'] = values.nsmallest(values.size - topk).sum()

    key_df = pd.DataFrame({kdim: list(top_values.index), 'count': list(top_values.values)})[::-1]

    edata_key = hv.Dataset(data=key_df, kdims=[kdim])
    bars = hv.Bars(edata_key).relabel('%s count' % kdim).opts(invert_axes=True, width=600, height=400)

    return bars
    
from dash_table.Format import Sign
    
def price_tredency_plot_given(edata, kdim1="state", kdim2="CA"):
    """Holoview curve plot combined with pulldown widget of average price trendency of year given the k-dimension.

    Aggregate the data given the k-dimension and 'year'. Generate the curve plot with the pulldown widget.

    Args:
        arg1 (hv.Dataset): The hv.Dataset of the dataset
        arg2 (str): The key-dimension

    Returns:
        hv.element.chart.Curve: The holoview curve plot

    """
    assert isinstance(kdim1, str), "Please input your interested key dimension as string"
    assert isinstance(kdim2, str), "Please input your interested key value as string"

    edata = edata[(edata['year']>=2000) & (edata['year']<=2021)]
    edata = edata[edata[kdim1] == kdim2]

    agg = edata.aggregate('year', function=np.mean, spreadfn=np.std).sort()
    plot = hv.Curve(agg).opts(width=1000, height=450)

    return plot


def get_count_cols(df):
    """Get the columns for the count plot.

    Select the columns with object and category data types and return them as a list.

    Args:
        df (pd.DataFrame): The pd.DataFrame of the dataset

    Returns:
        List: The columns for the count plot

    """

    cols = list(df.select_dtypes(['object', 'category']).columns)

    return cols


def get_price_trendency_cols(df):
    """Get the columns for the price trendency plot.

    Select the columns with object and category data types and return them as a list.

    Args:
        df (pd.DataFrame): The pd.DataFrame of the dataset

    Returns:
        List: The columns for the count plot

    """
    cols = list(df.columns)
    cols.remove('price')
    cols.remove('region')
    cols.remove('model')
    cols.remove('posting_date')
    cols.remove('posting_year')
    cols.remove('posting_month')

    return cols

def get_price_trendency_given_cols(df):
    """Get the columns for the price trendency plot.

    Select the columns with object and category data types and return them as a list.

    Args:
        df (pd.DataFrame): The pd.DataFrame of the dataset

    Returns:
        List: The columns for the count plot

    """
    cols = list(df.columns)
    cols.remove('price')
    cols.remove('year')
    cols.remove('region')
    cols.remove('model')
    cols.remove('posting_date')
    cols.remove('posting_year')
    cols.remove('posting_month')

    return cols


def get_price_trendency_given_vals(df, kdim):
    """Get the values of the sepcific key-dimension

    Given the columns, get all values in this columns and return as a list.

    Args:
        df (pd.DataFrame): The pd.DataFrame of the dataset
        kim (str): The key-dimension

    Returns:
        list: The values given the specific cols

    """

    vals = list(set(df.dropna()[kdim].tolist()))

    return vals



def statewise_prices(df):
    """
    TODO
    """
    p = df.groupby(['state']).mean().price
    statewise_prices = pd.DataFrame({'states':p.index, 'avg_price':p.values}) 
    statewise_prices['states'] = statewise_prices['states'].str.upper()

    fig = px.choropleth(statewise_prices, locations='states', locationmode="USA-states",  
                           color='avg_price',
                           range_color=(10000, 35000),
                           scope="usa",
                           color_continuous_scale="Blues"
                          )
    return fig

def plot_pie(df, col, cats, lim = 15):
    """Plots the pie chart of the categorical variable col.

    The col variable must be the name of a categorical column of the dataframe.
    From there, it will create a pie chart of the most frequent values up to lim.
    All other values will be assigned to the 'Other' group.

    Args:
        df: The dataframe
        col (str): The name of the categorical column.
        cats: The set of categorical columns (used only for checks)
        lim (int): The top number of values to group by.
    """
    assert col in cats

    values = df[col].dropna().value_counts().sort_values(ascending=False)
    topk = min(len(values), lim)
    top_values = values.nlargest(topk)
    if len(values) > lim: top_values['other'] = values.nsmallest(values.size - topk).sum()
    title = 'Number of cars by %s:' % (col.replace('_', ' '))
    fig = px.pie(values, values=top_values.values, names=top_values.index, title=title,color_discrete_sequence=px.colors.sequential.RdBu)

    return fig
