'''
This file tests the functions in layout.py.
To generate a html coverage report, run
pytest --cov-report html:cov_html
        --cov=carsreco
'''
import pytest
import numpy as np
import dash.html as html
import dash.dcc as dcc
import pandas as pd
from carsreco import layout, prediction, interactive_plots

@pytest.fixture()
def setup():
    """Creates a mock dataframe for setting up the layout.
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

def test_layout_class(setup):
    """Tests the initialization of the Layout class.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    model = prediction.IntervalPricePrediction(mock_df)
    app = layout.Layout(mock_df, model)
    assert all([isinstance(att, html.Div) for att in [app.full_layout,
                                                      app.tab_1,
                                                      app.tab_2]])
    children = app.full_layout.children
    assert len(children) == 3
    assert all([isinstance(child, (html.Div, html.H1, dcc.Tabs)) for child in children])
    assert all([isinstance(child1, html.Div) for child1 in app.tab_1.children])
    assert all([isinstance(child2, html.Div) for child2 in app.tab_2.children])

def test_dropdown_and_plot(setup):
    """Tests the dropdown_and_plot function.

    Args:
        setup (pd.DataFrame): The test dataframe.
    """
    mock_df = setup
    li1 = interactive_plots.get_price_trendency_cols(mock_df)
    dropdown_plot1 = layout.dropdown_and_plot(li1, "1", 430)
    assert isinstance(dropdown_plot1, html.Div) and li1 is dropdown_plot1.children[0].options
    li2 = interactive_plots.get_count_cols(mock_df)
    dropdown_plot2 = layout.dropdown_and_plot(li2, "2", 900)
    assert isinstance(dropdown_plot2, html.Div) and li2 is dropdown_plot2.children[0].options
    li_out = interactive_plots.get_price_trendency_given_cols(mock_df)
    dropdown_out = layout.dropdown_and_plot(li_out, "-out")
    assert isinstance(dropdown_out, html.Div) and li_out is dropdown_out.children[0].options
