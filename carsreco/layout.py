from .css import *
from .data import df
from .interactive_plots import get_count_cols, get_price_trendency_cols, \
    get_price_trendency_given_cols, statewise_prices

import dash_html_components as html
import dash_core_components as dcc




full_layout = html.Div(
    children = [
        html.H1("Used Car Sales Recommendation Dashboard", style=H1_style), #bed2ff, 2ddfb3
        dcc.Tabs(id="tabs", value='tab-1', style={'margin-top': '0em', 'margin-bottom': '0em'},
        children=[
            dcc.Tab(label='Cars Sales Information & Trends',
                    value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Find Your Dream Car!', value='tab-new', 
                    style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs-content')
])


li1 = get_price_trendency_cols(df)
li2 = get_count_cols(df)
li_out = get_price_trendency_given_cols(df)

dropdown_plot1 = html.Div(
    children =[
        dcc.Dropdown(li1, id='dd-input1', 
                     placeholder='Select an attribute...', 
                     style=dropdown_style),
    html.Div(
        children =[
            html.Div(
                id='dd-output1',
                style={'height': 430, **plot_style}
            )
        ]
    ),
    ],
    style=plot_div_style
)


dropdown_plot2 = html.Div(
    children =[
    dcc.Dropdown(
        li2, 
        id='dd-input2', 
        placeholder='Select an attribute...', 
        style=dropdown_style
    ),
    html.Div(
        id='dd-output2',
        style={'float': 'center', 'height': 900, 'justify-content': 'center'}
    ),
    ]
)

dropdown_out = html.Div(
    children =[
        dcc.Dropdown(
            li_out, 
            id='dd-input-out', 
            placeholder='Select an attribute...', 
            style=dropdown_style
        ),
        html.Div(
            id='dd-output-out',
            style={'width':'100%'}
        )
    ],
    style=level3_div_style
)


def dropdown_in(li_in: list) -> html.Div:
    """dropdown generator

    creates a dropdown from a list

    Args:
        li_in: list of inputs for 

    Returns:
        html.Div: a div containing the dropdown
    """
    dd = html.Div(
        children =[
            dcc.Dropdown(li_in, 
                id='dd-input-in', placeholder='Select an attribute...', 
                style=dropdown_style
            ),
            html.Div(
                id='dd-output-in',
                style={"width": "100%"}
            )
        ]
    )
    return dd

# THIS IS NOT THE WHOLE LAYOUT BUT THE LAYOUT OF FIRST TAB
# WHOEVER LIKES REFACTORING RENAME THIS
whole_layout = html.Div(
    style=toplevel_div_style,
    children=[
            html.Div(
                children=[
                    html.H3("The Market Share Overview:", style=H3_style),
                    dropdown_plot2,
                ],
                style=level2_div_style
            ),

            html.Div([
                html.H3("Average Price Trendency over Time:", style=H3_style),
                dropdown_plot1
            ],
            style = level2_div_style
            ),

            html.Div(
                [
                    html.H3("Average Price Across States:", style=H3_style),
                    html.Div(
                        children =[
                            dcc.Graph(
                                id = "marital prob",
                                figure = statewise_prices(df),
                                style={'height': 450, 'justify-content': 'center'}
                            )
                        ],
                    ),
                ],
                style=level2_div_style
            ),

            html.Div(
                [
                    html.H3("Explore the Price Fluctuation of Your Interest:", style=H3_style),
                    dropdown_out
                ],
                style=level2_div_style
            ),
]
)

