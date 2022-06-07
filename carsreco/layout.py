import functools as ft

from dash.development.base_component import Component
import dash.html as html
import dash.dcc as dcc
import pandas as pd

from .css import *
from .interactive_plots import get_count_cols, get_price_trendency_cols, \
    get_price_trendency_given_cols, statewise_prices
from . import prediction

Div = ft.partial(html.Div, style=div_style)
H1 = ft.partial(html.H1, style=H1_style)
H3 = ft.partial(html.H3, style=H3_style)
Tab = ft.partial(dcc.Tab, style=tab_style, selected_style=tab_selected_style)
Dropdown=ft.partial(dcc.Dropdown, placeholder='Select an attribute...', style=dropdown_style )
Tabs=ft.partial(dcc.Tabs, style=tabs_style)


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
    """

    full_layout: Component
    dropdown_plot1: Component
    dropdown_plot2: Component
    dropdown_out: Component

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

        self.dropdown_plot1 = dropdown_and_plot(li1, "1", 430)

        self.dropdown_plot2 = dropdown_and_plot(li2, "2", 900)

        self.dropdown_out = dropdown_and_plot(li_out, "-out")


        # THIS IS NOT THE WHOLE LAYOUT BUT THE LAYOUT OF FIRST TAB
        # WHOEVER LIKES REFACTORING RENAME THIS TODO
        self.tab_1 = html.Div(
            style=toplevel_div_style,
            children=[
                    Div([
                        H3("The Market Share Overview:"),
                        self.dropdown_plot2,
                    ]),
                    Div([
                        H3("Average Price Trend over Time:"),
                        self.dropdown_plot1
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
                        self.dropdown_out
                    ]),
            ]
        )

        # THIS IS THE LAYOUT OF THE SECOND TAB
        self.tab_2  = html.Div(
            children=[
                html.Div(
                    children=[
                        html.Label('Select your preferred model: ', style=label_style),
                        dcc.Dropdown(
                            list(p.get_manufacturer_names()),
                            id='model-dd',
                            placeholder='Select an attribute...',
                            style={**dropdown_style, "margin":"auto"}
                        ),
                        html.Label('Select your preferred year range: ', style=label_style), # next available witnin 
                        html.Div(dcc.RangeSlider(
                            id='year-range-slider',
                            min=1999,
                            max=2020,
                            value=[2005, 2015],
                            allowCross=False,
                            marks={int(i):str(i) for i in range(1999, 2020, 5)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                                 style=slider_style
                                 ),
                        html.Label('Select your preferred price range ($): ', style=label_style),
                        html.Div(dcc.RangeSlider(
                            id='price-range-slider',
                            min=3000,
                            max=80000,
                            value=[15000, 25000],
                            allowCross=False,
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                                 style=slider_style
                                 ),
                    ], 
                    id="preferences-div", 
                    style={**level2_div_style, **container, "justify-content": "center"}
                ),
                html.Div(
                    children=[
                        html.H1(children='Recommendation to You', style=H3_style_2),
                        html.Hr(), 
                        html.Div(id='pred-output')
                    ], 
                    style={'textAlign': 'center', 'justify-content': 'center', 'margin-top': '3em'}),
            ], 
            style=toplevel_div_style
        )
