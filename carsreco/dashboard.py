"""
This file contains the web application logic
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash
import numpy as np
import pandas as pd
import plotly.express as px

from .data import df
from .interactive_plots import interactive_plots_preprocess, price_trendency_plot, count_plot, price_tredency_plot_given,  get_price_trendency_given_vals
from . import prediction
from .layout import *
from .wikipedia_api import WikipediaPage

external_stylesheets = ['assets/style.css'] #https://codepen.io/chriddyp/pen/bWLwgP.css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #external_stylesheets=external_stylesheets

app.config['suppress_callback_exceptions'] = True

app.layout = full_layout

#------------------------------------------------------------------------------------
# PREPROCESSING
#------------------------------------------------------------------------------------
edata = interactive_plots_preprocess(df)
cats, nums = df.select_dtypes(['object', 'category']).columns, df.select_dtypes(np.number).columns
p = prediction.IntervalPricePrediction(df)

def plot_pie(col, lim = 15):
    """Plots the pie chart of the categorical variable col.

    The col variable must be the name of a categorical column of the dataframe.
    From there, it will create a pie chart of the most frequent values up to lim.
    All other values will be assigned to the 'Other' group.

    Args:
        col (str): The name of the categorical column.
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

#***************************** DropDown

def dropdown_select(k):
    components = to_dash(app, [price_trendency_plot(edata, k)])
    plot = html.Div(components.children)
    return plot

def dropdown_count(k):
    components = to_dash(app, [count_plot(df, k)])
    plot = html.Div(children=[
            html.Div(components.children),
            html.Div(
                dcc.Graph(
                id = "dd-pie",
                figure = plot_pie(k),
                style={'justify-content': 'center', 'margin-top':'1em'})
    )])
    return plot

def dropdown_given(k1, k2):
    components = to_dash(app, [price_tredency_plot_given(edata, k1, k2)])
    plot = html.Div(components.children)
    return plot


### DropDown ###



@app.callback(
    Output('dd-output1', 'children'),
    Input('dd-input1', 'value')
)
def update_output(value):
    if not value:
        return dropdown_select("state")
    return dropdown_select(value)



@app.callback(
    Output('dd-output2', 'children'),
    Input('dd-input2', 'value')
)
def update_output(value):
    if not value:
        return dropdown_count("manufacturer")
    return dropdown_count(value)



@app.callback(
    Output('dd-output-in', 'children'),
    [Input('dd-input-in', 'value'),
     Input('dd-input-out', 'value')]
)
def update_output(value_in, value_out):
    if not value_out:
        return dropdown_given("state", "CA")
    elif not value_in:
        return dropdown_given(value_out, get_price_trendency_given_vals(df, value_out)[0])
    return dropdown_given(value_out, value_in)

@app.callback(
    Output('dd-output-out', 'children'),
    Input('dd-input-out', 'value')
)
def update_output(value):
    if not value:
        value = "state"
    li_in = get_price_trendency_given_vals(df, value)
    return dropdown_in(li_in)




def text_image(lisa,urll,i):
    return html.H1('Manufacturer name: ' + lisa[i][0] + ", Model name: " + str(lisa[i][1]) + ", Find it at market in  " + str(lisa[i][3:]) + " hrs",
            style={'color': '#b8bbbe', 'font-size': '24px', 'font-family': 'Optima, sans-serif','font-weight':'bold'}), html.Img(src=urll[i], style={'height': '40%', 'width': '40%'})

layout_tab_new = html.Div(children=[
    html.Label('Select your preferred model: ', style=label_style),
    html.Div(dcc.Dropdown(list(p.get_manufacturer_names()),
                          id='model-dd', placeholder='Select an attribute...', style={'width': '60%'}
                          ),
             style={'float': 'center', 'justify-content': 'center','margin-left':'40em'}
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
        style={'width': '50%','float': 'center','justify-content': 'center', 'margin-top': '2em', 'margin-left':'25em'}
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
        style={'width': '50%', 'float': 'center','justify-content': 'center','margin-top': '2em', 'margin-left':'25em'}
    ),
    html.Div(children=[
        html.H1(children='- - - - - - - - - - - - - - - Recommendation to You - - - - - - - - - - - - - - -', style=H3_style_2),
        html.Div(id='pred-output')
    ], style={'textAlign': 'center', 'justify-content': 'center', 'margin-top': '3em'}),
])

@app.callback(
    Output('pred-output', 'children'),
    [Input('model-dd', 'value'),
     Input('year-range-slider', 'value'),
     Input('price-range-slider', 'value')])
def show_success_probability(model,year,price):
    if not model:
        recommended_cars = p.get_CI(price[0], price[1])
    else:
        recommended_cars = p.get_CI(price[0], price[1], [model])
    lisa = [list(c) for c in recommended_cars]
    urll = []
    for item in lisa:
        page = WikipediaPage.from_query(item[0]+"_"+item[1])
        urll.append(page.get_thumbnail()['source'])

    ccc = html.H3(str('''Manufacturer Name, Model name, Time: 95% confidence interval of time for the next post of given model within desired price range'''), style=label_style),

    childs = []
    childs.append(ccc)
    if lisa:
        for i in range(len(lisa)):
            a,b = text_image(lisa,urll,i)
            childs.append(a)
            childs.append(b)
    else:
        childs.append(html.H3(("Sorry, no car found within your price range"),style = sorry_style)) #fea78a

    return html.Div(children= [html.Ul(children=[html.Li(i) for i in childs])])

        
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return whole_layout
    elif tab == "tab-new":
        return layout_tab_new

server = app.server

if __name__ == '__main__':
    app.run_server(host="0.0.0.0")
