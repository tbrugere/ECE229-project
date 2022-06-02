import numpy as np
import pandas as pd

import holoviews as hv

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
    
def price_tredency_plot_given(edata, kdim):
    """Holoview curve plot combined with pulldown widget of average price trendency of year given the k-dimension.

    Aggregate the data given the k-dimension and 'year'. Generate the curve plot with the pulldown widget.

    Args:
        edata (hv.Dataset): The hv.Dataset of the dataset
        kdim (str): The key-dimension

    Returns:
        hv.core.spaces.HoloMap: The holoview curve plot with the pulldown widget

    """
    assert isinstance(kdim, str), "Please input your interested key dimension as string"

    edata = edata[(edata['year']>=2000) & (edata['year']<=2021)]
    agg = edata.aggregate(['year', kdim], function=np.mean).sort()
    plot = agg.to(hv.Curve, 'year', 'price', groupby=kdim).options(width=600,height=300, title='Average Price Fluctuation over year given %s' % kdim)

    return plot
