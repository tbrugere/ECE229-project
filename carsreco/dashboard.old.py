import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
from dash_table.Format import Sign
from . import prediction

external_stylesheets = ['assets/style.css'] #https://codepen.io/chriddyp/pen/bWLwgP.css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #external_stylesheets=external_stylesheets

# app.scripts.config.serve_locally = True

app.config['suppress_callback_exceptions'] = True

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
tab_style = {
    'borderTop': '1px solid #292841',
    'borderBottom': '1px solid #292841',
    'borderLeft': '1px solid #bcbfc2',
    'borderRight': '1px solid #bcbfc2',
    'fontWeight': 'bold',
    'font-size': '20px',
    'font-family': 'Optima, sans-serif',
    'color': '#b8bbbe',
    'backgroundColor': '#292841',
    'padding': '8px',
}

tab_selected_style = {
    'borderTop': '2px solid #bed2ff',
    'borderBottom': '1px solid #292841',
    'borderLeft': '1px solid #bcbfc2',
    'borderRight': '1px solid #bcbfc2',
    'backgroundColor': '#292841',
    'color': 'white',
    'font-size': '22px',
    'font-family': 'Optima, sans-serif',
    'font-weight': 'bold',
    'padding': '8px',
}

H3_style = {
    'font-family': 'Optima, sans-serif',
    'font-size': '28px',
    'color': '#bed2ff',
    'font-weight': 'bold',
    'float': 'center',
    'text-align': 'center',
    'margin-top': '1em',
    # 'margin-bottom': '1em',
}

H3_style_2 = {
    'font-family': 'Optima, sans-serif',
    'font-size': '48px',
    'color': '#bed2ff',
    'font-weight': 'bold',
    'float': 'center',
    'text-align': 'center',
    'margin-top': '2em',
    # 'margin-bottom': '1em',
}

label_style = {
    'font-family': 'Optima, sans-serif',
    'font-size': '24px',
    'color': '#bed2ff',
    'font-weight': 'bold',
    'float': 'bottom',
    # 'margin-left': '1em',
    'margin-top': '1em',
    'margin-bottom': '0.5em',
    'text-align': 'center',
}

sorry_style = {
    'font-family': 'Optima, sans-serif',
    'font-size': '24px',
    'color': '#fea78a',
    'font-weight': 'bold',
    'float': 'bottom',
    # 'margin-left': '1em',
    'margin-top': '1em',
    'margin-bottom': '3em',
    'text-align': 'center',
}

app.layout = html.Div(
    children = [
    html.H1("Used Car Sales Recommendation Dashboard", style={'text-align': 'center', 'font-family': 'Optima, sans-serif',
                                                              'padding-top': '0.4em', 'padding-bottom': '0.4em',
                                                              'margin-top': '0em', 'margin-bottom': '0em',
                                                              'font-weight': 'bold', 'color': '#bed2ff', 'font-size': '40px',
                                                              'backgroundColor':'#292841'}), #bed2ff, 2ddfb3
    dcc.Tabs(id="tabs", value='tab-1', style={'margin-top': '0em', 'margin-bottom': '0em'},
        children=[
        dcc.Tab(label='Cars Sales Information & Trends', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Find Your Dream Car!', value='tab-new', style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs-content')
])

df: pd.DataFrame = pd.read_csv('data/preprocessed.csv', header=0, index_col=0)#type: ignore
cats, nums = df.select_dtypes(['object', 'category']).columns, df.select_dtypes(np.number).columns

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

def statewise_prices(df):
    """
    
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
#***************************** DropDown

from .interactive_plots import interactive_plots_preprocess, price_trendency_plot, count_plot, price_tredency_plot_given, get_count_cols, get_price_trendency_cols, get_price_trendency_given_cols, get_price_trendency_given_vals
import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash

li1 = get_price_trendency_cols(df)
li2 = get_count_cols(df)
li_out = get_price_trendency_given_cols(df)
edata = interactive_plots_preprocess(df)

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


dropdown_plot1 = html.Div(children =[
    dcc.Dropdown(li1, 
        id='dd-input1', placeholder='Select an attribute...', style={'float': 'center','width': '50%'}),
    html.Div(children =[
        html.Div(id='dd-output1',style={'float': 'center', 'height': 430,'width': 1200, 'justify-content': 'center'})]),],
    style={'margin-left': '8em', 'float': 'center', 'justify-content': 'center'})

@app.callback(
    Output('dd-output1', 'children'),
    Input('dd-input1', 'value')
)
def update_output(value):
    if not value:
        return dropdown_select("state")
    return dropdown_select(value)


dropdown_plot2 = html.Div(children =[
    dcc.Dropdown(li2, 
        id='dd-input2', placeholder='Select an attribute...', style={'width': '50%'}),
    html.Div(children =[
        html.Div(id='dd-output2',style={'float': 'center', 'height': 900,'width': 800, 'justify-content': 'center'}),
        ]),],
    style={'float': 'center', 'justify-content': 'center', 'margin-left':'21em'})

@app.callback(
    Output('dd-output2', 'children'),
    Input('dd-input2', 'value')
)
def update_output(value):
    if not value:
        return dropdown_count("manufacturer")
    return dropdown_count(value)


def dropdown_in(attri):
    li_in = get_price_trendency_given_vals(df, attri)
    dd = html.Div(children =[
        dcc.Dropdown(li_in, 
            id='dd-input-in', placeholder='Select an attribute...', style={'width': '80%', 'margin-left': '3.5em'}),
        html.Div(children =[
            html.Div(id='dd-output-in',style={'height': 490,'width': 900, 'float': 'center', 'display': 'flex', 'justify-content': 'center'})]),],
        style={'float': 'center', 'justify-content': 'center'})
    return dd

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

dropdown_out = html.Div(children =[
    dcc.Dropdown(li_out, 
        id='dd-input-out', placeholder='Select an attribute...', style={'width': '60%', 'margin-left': '12.7em'}),
    html.Div(children =[
        html.Div(id='dd-output-out',style={'float': 'center', 'display': 'flex', 'justify-content': 'center'})]),
    ],
    style={'float': 'center', 'justify-content': 'center'})

@app.callback(
    Output('dd-output-out', 'children'),
    Input('dd-input-out', 'value')
)
def update_output(value):
    if not value:
        return dropdown_in('state')
    return dropdown_in(value)


whole_layout = html.Div(style={'margin-left':'2em', 'margin-right':'2em'},
    children =[
        html.Div([
            html.Div([
                html.H3("The Market Share Overview:", style=H3_style),
                dropdown_plot2,
            ]),

            html.Div([
                html.H3("Average Price Trendency over Time:", style=H3_style),
                dropdown_plot1,
            ]),

            html.Div([
                html.H3("Average Price Across States:", style=H3_style),
                html.Div(children =[
                    dcc.Graph(
                    id = "marital prob",
                    figure = statewise_prices(df),
                    style={'height': 450,'width': 800, 'justify-content': 'center'}
                )],
            style={'height': 480, 'float': 'center', 'display': 'flex', 'justify-content': 'center'}),
            ]),

            html.H3("Explore the Price Fluctuation of Your Interest:", style=H3_style),
            dropdown_out,
        ]),
    ])


p = prediction.IntervalPricePrediction(df)
from .wikipedia_api import WikipediaPage
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
