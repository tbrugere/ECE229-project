"""
This module contains the (html) layout of the application. It also contains helper functions
used to generate the dynamic layout of the application.

This module does not contain the plots definitions, those are created in the :module:`carsreco.interactive_plots` module.

It also does not contan the application logic, this is contained in :module:`carsreco.dashboard`
"""

from __future__ import annotations

import functools as ft

from dash.development.base_component import Component
import dash.html as html
import dash.dcc as dcc
import pandas as pd

from .css import *
from .interactive_plots import get_count_cols, get_price_trendency_cols, \
    get_price_trendency_given_cols, statewise_prices
from . import prediction

###############################################
#Apply CSS without CSS
###############################################

Div = ft.partial(html.Div, style=div_style)
H1 = ft.partial(html.H1, style=H1_style)
H3 = ft.partial(html.H3, style=H3_style)
Tab = ft.partial(dcc.Tab, style=tab_style, selected_style=tab_selected_style)
Dropdown=ft.partial(dcc.Dropdown, placeholder='Select an attribute...', style=dropdown_style )
Tabs=ft.partial(dcc.Tabs, style=tabs_style)
Label = ft.partial(html.Label, style=label_style)

def Slider(*args, **kwargs) -> html.Div:
    """create a slider

    Creates a :class:`html.Div` containing a :class:`dcc.Slider`, with the right styling

    Returns:
        html.Div: said div
    """
    return html.Div( dcc.RangeSlider(*args, **kwargs), style=slider_style )


def text_image(item: list, url: str) -> tuple[html.H3, html.Img]:
    """Generates markup for a prediction result

    Generates the text representing a prediction in a h3, as well as a tag containing 
    the image from the url given.
    This is used to display predictions from the model.

    Args:
        item: a list containing one item of the predictions results
        url: the url of the corresponing image

    Returns:
        tuple[html.H3, html.Img]: [TODO:description]
    """
    return (
        html.H3(
        f'Manufacturer name: {item[0]}, Model name: {item[1]}, Find it at market in {item[2]} hrs', 
        style=text_image_style),
        html.Img(src=url, style={'height': '40%', 'width': '40%'})
    )


def dropdown_and_plot(l: list, id: str, plot_height=None) -> html.Div:
    """dropdown generator

    creates a dropdown from a list, and a plot related to that dropdown

    Args:
        l: list of inputs for the dropdown
        id: the dropdown will have id=dd-input{id}, the plot 

    Returns:
        html.Div: a div containing the dropdown
    """

    return Div(
        children =[
            Dropdown(l, id=f'dd-input{id}'),
            html.Div(id=f'dd-output{id}',
                style=(plot_style if plot_height is None 
                       else {"height": plot_height, **plot_style}))
        ]
    )


class Layout():
    """Layout of the application


    Attributes:
        full_layout: the layout of the entire page

        tab_1: the layout fo the first tab
        tab_2: the layout fo the second tab
    """

    full_layout: Component

    tab_1: Component
    tab_2: Component

    def __init__(self, df: pd.DataFrame, model: prediction.IntervalPricePrediction): 
        p = model
        li1 = get_price_trendency_cols(df)
        li2 = get_count_cols(df)
        li_out = get_price_trendency_given_cols(df)

        self.full_layout = Div(
            children = [
                H1("Used Car Sales Recommendation Dashboard"), 
                Tabs(
                    id="tabs",
                    value='tab-1', 
                    children=[
                        Tab(label='Cars Sales Information & Trends', value='tab-1'),
                        Tab(label='Find Your Dream Car!', value='tab-new' ),
                    ]
                ),
            html.Div(id='tabs-content')
            ]
        )

        dropdown_plot1 = dropdown_and_plot(li1, "1", 430)

        dropdown_plot2 = dropdown_and_plot(li2, "2", 900)

        dropdown_out = dropdown_and_plot(li_out, "-out")


        self.tab_1 = html.Div(
            style=toplevel_div_style,
            children=[
                    Div([
                        H3("The Market Share Overview:"),
                        dropdown_plot2,
                    ]),
                    Div([
                        H3("Average Price Trend over Time:"),
                        dropdown_plot1
                    ]),

                    Div([
                        H3("Average Price Across States:"),
                        html.Div(
                            children =[
                                dcc.Graph(
                                    id = "marital prob",
                                    figure = statewise_prices(df),
                                    style={'height': 450, 'justify-content': 'center'}
                                )
                            ],
                        ),
                    ]),
                    Div([
                        H3("Explore the Price Fluctuation of Your Interest:"),
                        dropdown_out
                    ]),
            ]
        )

        # THIS IS THE LAYOUT OF THE SECOND TAB
        self.tab_2  = html.Div(
            children=[
                html.Div(
                    children=[
                        Label('Select your preferred model: '),
                        dcc.Dropdown(
                            list(p.get_manufacturer_names()),
                            id='model-dd',
                            placeholder='Select an attribute...',
                            style={**dropdown_style, "margin":"auto"}
                        ),
                        Label('Select your preferred year range: '), 
                        Slider(
                                id='year-range-slider',
                                min=1999,
                                max=2020,
                                value=[2005, 2015],
                                allowCross=False,
                                marks={int(i):str(i) for i in range(1999, 2020, 5)},
                                tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        Label('Select your preferred price range ($): '),
                        Slider(
                            id='price-range-slider',
                            min=3000,
                            max=80000,
                            value=[15000, 25000],
                            allowCross=False,
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], 
                    id="preferences-div", 
                    style={**level2_div_style, **container, "justify-content": "center"}
                ),
                html.Div(
                    children=[
                        H1(children='Recommendation to You'),
                        html.Hr(),
                        Div(id='pred-output')
                    ], 
                    style={'textAlign': 'center', 'justify-content': 'center', 'margin-top': '3em'}),
            ], 
            style=toplevel_div_style
        )
