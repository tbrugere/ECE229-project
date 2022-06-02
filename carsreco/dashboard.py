import dash
#from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
#from scripts import preprocessing
from .interactive_plots import *

from holoviews.plotting.plotly.dash import to_dash

from .plot_analysis import *
# from visualization import plots
# from data import plot_analysis

external_stylesheets = ['assets/style.css']  # https://codepen.io/chriddyp/pen/bWLwgP.css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # external_stylesheets=external_stylesheets

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
    'font-size': '45px',
    'color': '#bed2ff',
    'font-weight': 'bold',
    'float': 'center',
    #'margin_top': '1.67em',
    #'margin_bottom': '1.67em',
    'text-align': 'center',
}
H3_style_r = {
    'font-family': 'Optima, sans-serif',
    'font-size': '40px',
    'color': '#bed2ff',
    'font-weight': 'bold',
    'float': 'left',
    'text-align': 'center',
}

label_style = {
    'font-family': 'Optima, sans-serif',
    'font-size': '20px',
    'color': '#bed2ff',
    'font-weight': 'bold',
    'float': 'bottom',
    'margin-left': '1em',
    # 'text-align': 'center',
}

app.layout = html.Div(
    children=[
        html.H1("Used Car Sales Recommendation Dashboard",
                style={'text-align': 'center', 'font-family': 'Optima, sans-serif',
                       'padding-top': '0.4em', 'padding-bottom': '0.4em',
                       'margin-top': '0em', 'margin-bottom': '0em',
                       'font-weight': 'bold', 'color': '#bed2ff', 'font-size': '40px',
                       'backgroundColor': '#292841'}),  # bed2ff, 2ddfb3
        dcc.Tabs(id="tabs", value='tab-1', style={'margin-top': '0em', 'margin-bottom': '0em'},
                 children=[
                     dcc.Tab(label='Car Sales Information & Trends', value='tab-1', style=tab_style,
                             selected_style=tab_selected_style),
                     dcc.Tab(label='Cars Recommendation Dashboard', value='tab-new', style=tab_style,
                             selected_style=tab_selected_style),
                 ]),
        html.Div(id='tabs-content')
    ])  # style={'backgroundColor':'#cbd4ff'}


df_A = pd.read_csv('data/preprocessed.csv')
cats, nums = df_A.select_dtypes(['object', 'category']).columns, df_A.select_dtypes(np.number).columns


def state_average():
    fig = px.choropleth(get_groupby_columns('state', 'price', 'mean',df=df_A), locations='state', locationmode="USA-states",
                        color='price',
                        # color_continuous_scale="Viridis",
                        scope="usa",
                        color_continuous_scale=px.colors.sequential.Plasma
                        )
    return fig


edata = interactive_plots_preprocess(df_A)


def dropdown_select(k,edata = edata):
    components = to_dash(app, [price_trendency_plot(edata, k)])
    plot = html.Div(components.children)
    return plot
def dropdown_count(k,df = df_A):
    components = to_dash(app, [count_plot(df, k)])
    plot = html.Div(components.children)
    return plot

def dropdown_given(k,edata = edata):
    components = to_dash(app, [price_tredency_plot_given(edata, k)])
    plot = html.Div(components.children)
    return plot



### DropDowns Div###
dropdown_plot = html.Div(children=[
    dcc.Dropdown(
        ['year', 'state', 'manufacturer', 'model', 'condition', 'odometer', 'fuel', 'size', 'type', 'cylinders',
         'drive', 'transmission', 'paint_color', 'price_range', 'year_range', 'odometer_range'],
        id='demo-dropdown', placeholder='Select an attribute...', style={'justify-content': 'center', 'width': '100%'}),
        html.Div(id='dd-output-container',
                 style={'height': 380, 'width': '280', 'justify-content': 'center'})],
        )  # bottom of H3 / no flex

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    if not value:
        return dropdown_select("year")
    return dropdown_select(value)


dd_count = html.Div(children =[
    dcc.Dropdown(['year', 'state', 'manufacturer', 'model', 'condition', 'odometer', 'fuel', 'size', 'type', 'cylinders', 'drive', 'transmission', 'paint_color', 'price_range','year_range', 'odometer_range'],
    id='count-dropdown', placeholder='Select an attribute...', style={'justify-content': 'center','width': '100%'}),
    html.Div(id='count-output-container',style={'height': 380, 'width': '280', 'justify-content': 'center'})],
    )

@app.callback(
    Output('count-output-container', 'children'),
    Input('count-dropdown', 'value')
)
def update_output(value):
    if not value:
        return dropdown_count("manufacturer")
    return dropdown_count(value)

dd_given = html.Div(children =[
    dcc.Dropdown(['year', 'state', 'manufacturer', 'model', 'condition', 'odometer', 'fuel', 'size', 'type', 'cylinders', 'drive', 'transmission', 'paint_color', 'price_range','year_range', 'odometer_range'],
    id='count-dropdown_given', placeholder='Select an attribute...', style={'justify-content': 'center','width': '100%'}),
    html.Div(id='given_t',style={'height': 380, 'width':'280', 'justify-content': 'center'})],
    )

@app.callback(
    Output('given_t', 'children'),
    Input('count-dropdown_given', 'value')
)
def update_output(value):
    if not value:
        return dropdown_given("year")
    return dropdown_given(value)

#######
#Information(graphs) Dashoard implmented here!!
#######
marital_status_vis = html.Div(style={'margin-left': '2em', 'margin-right': '2em'},
                              children=[
                                  html.Div([
                                      html.H3(children="Prices:",style=H3_style),
                                      html.Div(children=[
                                          dcc.Graph(
                                              id="marital status",
                                              figure=plot_pie('price_range',df=df_A)
                                          )],
                                          style={'height': 380, 'width': '280', 'float': 'center', 'display': 'flex',
                                                 'justify-content': 'center'}),

                                      html.H3(children="States Overview:", style=H3_style),
                                      html.Div(children=[
                                          #html.H3(children="States Overview:", style=H3_style),
                                          dcc.Graph(
                                              id="marital prob",
                                              figure=state_average()
                                          )],
                                          style={'height': 380, 'width': '280', 'float': 'center', 'display': 'flex',
                                                 'justify-content': 'center'}),
                                  ]),

                                  # dropdown_plot,
                                  html.Div([
                                      html.H3(children="price trendency", style=H3_style),
                                      dropdown_plot,

                                      html.H3(children="Count Plot:", style=H3_style),
                                      dd_count,

                                      html.H3(children="year trendency", style=H3_style),
                                      dd_given,
                                  ]),

                              ])


#######
#recomendation Dashoard implmented here!!
#######
layout_tab_new = html.Div(children=[
    html.Label('Select your preferred model: ', style=label_style),
    html.Div(dcc.Dropdown(['gmc', 'toyota', 'ford', 'jeep', 'nissan', 'mazda'],
                          id='model-dd', placeholder='Select an attribute...', style={'width': '60%'}
                          ),
             style={'float': 'center', 'display': 'flex', 'justify-content': 'left', 'margin-left': '1em'}
             ),

    html.Label('Select your preferred year range: ', style=label_style),
    html.Div(dcc.RangeSlider(
        id='year-range-slider',
        min=1999,
        max=2020,
        value=[2005, 2015],
        allowCross=False,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
        style={'width': '50%', 'margin-top': '2em'}
    ),
    html.Label('Select your preferred price range: ', style=label_style),
    html.Div(dcc.RangeSlider(
        id='year-range-slider',
        min=3000,
        max=28000,
        value=[15000, 25000],
        allowCross=False,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
        style={'width': '50%', 'margin-top': '2em'}
    ),
    html.Div(children=[
        html.H1(children='Recommendation to You:', style=H3_style),
        html.Div(id='pred-output')
    ], style={'textAlign': 'center', 'justify-content': 'center', 'margin-top': '3em'}),
])


@app.callback(
    Output('pred-output', 'children'),
    [Input('nremployed', 'value'),
     Input('poutcome_success', 'value'),
     Input('emp', 'value'),
     Input('pdays', 'value'),
     Input('consconfidx', 'value'),
     Input('euribor3m', 'value'),
     Input('job_transformed_no_income', 'value')])

def show_success_probability(nr_employed, poutcome_success, emp_var_rate, pdays, cons_conf, euribor, no_income):
    if not nr_employed:
        nr_employed = 0
    if not poutcome_success:
        poutcome_success = 0
    if not emp_var_rate:
        emp_var_rate = 0
    if not pdays:
        pdays = 0
    if not cons_conf:
        cons_conf = 0
    if not euribor:
        euribor = 0
    if not no_income:
        no_income = 0

    return html.Div(children=[
        html.H1(children=f'{round(0.5, ndigits=2)}' + "%")
    ])





@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return marital_status_vis  # layout_whole
    elif tab == "tab-new":
        return layout_tab_new


server = app.server

if __name__ == '__main__':
    app.run_server(host="0.0.0.0")
