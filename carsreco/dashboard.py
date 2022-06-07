"""
This file contains the web application logic.
In other words, all callbacks for the dashboard components
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from holoviews.plotting.plotly.dash import to_dash
import pandas as pd

from .data import get_data, cats_and_nums, interactive_plots_preprocess
from .interactive_plots import price_trendency_plot, count_plot, price_tredency_plot_given,  get_price_trendency_given_vals, plot_pie
from . import prediction
from .layout import *
from .wikipedia_api import WikipediaPage

external_stylesheets = ['assets/style.css'] #https://codepen.io/chriddyp/pen/bWLwgP.css





### DropDown ###

def create_app() -> dash.Dash:
    """app factory

    Creates the app object that contains the application logic
    if app = create_app()
    then app.server can be passed to wsgi

    Returns:
        dash.Dash: the dash application.
    """
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.config['suppress_callback_exceptions'] = True

    df = get_data()
    cats, nums = cats_and_nums(df)
    edata = interactive_plots_preprocess(df)
    p = prediction.IntervalPricePrediction(df)

    layout = Layout(df, p)
    app.layout = layout.full_layout

    ################################################################
    # Dropdown functions
    ################################################################

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
                    figure = plot_pie(df, k, cats),
                    style={'justify-content': 'center', 'margin-top':'1em'})
        )])
        return plot

    def dropdown_given(k1, k2):
        components = to_dash(app, [price_tredency_plot_given(edata, k1, k2)])
        plot = html.Div(components.children)
        return plot

    ################################################################
    # Callbacks
    ################################################################


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
        drop = dropdown_and_plot(li_in, "-in")
        return drop





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
        predictions = [list(c) for c in recommended_cars]
        urll = []
        for item in predictions:
            page = WikipediaPage.from_query(item[0]+"_"+item[1])
            urll.append(page.get_thumbnail()['source'])

        ccc = html.H3(str('''Manufacturer Name, Model name, Time: 95% confidence interval of time for the next post of given model within desired price range'''), style=label_style),

        childs = []
        childs.append(ccc)
        if predictions:
            for pred, url in zip(predictions, urll):
                a,b = text_image(pred, url)
                childs.append(a)
                childs.append(b)
        else:
            childs.append(html.H3(("Sorry, no car found within your price range"),style = sorry_style)) #fea78a

        return html.Div(children= [html.Ul(children=[html.Li(i) for i in childs])])

            
    @app.callback(Output('tabs-content', 'children'),
                  [Input('tabs', 'value')])
    def render_content(tab):
        if tab == 'tab-1':
            return layout.tab_1
        elif tab == "tab-new":
            return layout.tab_2

    return app


if __name__ == '__main__':
    app = create_app
    app.run_server(host="0.0.0.0")
