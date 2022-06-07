'''
This file tests the functions in data.py and interactive_plots.py.
To generate a html coverage report, run
pytest --cov-report html:cov_html
        --cov=carsreco
'''
import pytest

import holoviews as hv
from plotly.graph_objs import Figure

import pandas as pd
from carsreco import data, layout, prediction, interactive_plots

@pytest.fixture()
def setup():
    """Creates a mock dataframe for setting up the interactive plots.
    """
    mock_df =  pd.DataFrame(columns=['year', 'state', 'region', 'model','manufacturer','price',
                                     'posting_date', 'posting_year','posting_month'],
                            data =[[2000, 'PA','greensboro', 'camry', 'abc',10000, '2021-05-04 17:30:00', 2021, 5],
                                   [2005, 'CA','hudson valley', 'silverado', 'def',7000, '2021-04-04 09:30:00', 2021, 4],
                                   [2010, 'CA','el paso', 'fx-150', 'ford', 12000, '2021-06-04 17:30:00', 2021, 5],
                                   [2015, 'WA','bellingham', 'camry', 'abc', 20000, '2021-06-04 16:30:00', 2021, 6],
                                   [2020, 'AL','auburn', 'camry', 'abc', 25000, '2021-05-04 09:30:00', 2021, 5],
                                   [2021, 'AL','birmingham', 'fx-150', 'ford', 15000, '2021-05-04 16:00:00', 2021, 5]])
    mock_df['posting_date'] = pd.to_datetime(mock_df['posting_date'])
    return mock_df

def test_get_data(setup):
    """Tests the get_data function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    df = data.get_data()
    assert isinstance(df, pd.DataFrame)

def test_interactive_plots_preprocess(setup):
    """Tests the interactive_plots_preprocess function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    predf = data.interactive_plots_preprocess(mock_df)
    assert isinstance(predf, hv.Dataset)

def test_cats_and_nums(setup):
    """Tests the cats_and_nums function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    cats, nums = data.cats_and_nums(mock_df)
    assert isinstance(cats, pd.Index) and set(cats).issubset(mock_df.columns)
    assert isinstance(nums, pd.Index) and set(nums).issubset(mock_df.columns)

def test_count_plot(setup):
    """Tests the count_plot function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    counts = interactive_plots.count_plot(mock_df)
    assert isinstance(counts, hv.element.chart.Bars)

def test_get_count_cols(setup):
    """Tests the get_count_cols function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    cols = interactive_plots.get_count_cols(mock_df)
    assert isinstance(cols, list) and set(cols).issubset(mock_df.columns)

def test_get_price_trendency_cols(setup):
    """Tests the get_price_trendency_cols function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    cols = interactive_plots.get_price_trendency_cols(mock_df)
    removed_cols = ['price', 'region', 'model',
                    'posting_date', 'posting_year', 'posting_month']
    assert isinstance(cols, list) and set(removed_cols).isdisjoint(cols)

def test_get_price_trendency_given_cols(setup):
    """Tests the get_price_trendency_given_cols function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    cols = interactive_plots.get_price_trendency_given_cols(mock_df)
    removed_cols = ['price', 'year', 'region', 'model',
                    'posting_date', 'posting_year', 'posting_month']
    assert isinstance(cols, list) and set(removed_cols).isdisjoint(cols)

def test_get_price_trendency_given_vals(setup):
    """Tests the get_price_trendency_given_vals function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    vals = interactive_plots.get_price_trendency_given_vals(mock_df, 'model')
    assert isinstance(vals, list)

def test_statewise_prices(setup):
    """Tests the statewise_prices function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    fig = interactive_plots.statewise_prices(mock_df)
    assert isinstance(fig, Figure)

def test_plot_pie(setup):
    """Tests the plot_pie function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    fig = interactive_plots.plot_pie(mock_df, 'state', mock_df.columns)
    assert isinstance(fig, Figure)