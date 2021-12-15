#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

# Attributes
attributes = ff_data.columns.values
attributes_options = [{'label': i, 'value': i} for i in attributes]

# Figures


# Dashboard

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(className="wrapper", children=[
        html.H1(id="myheadline", children="The World of Wines",
                style={'textAlign': 'center'})
    ]),
    
    html.div([
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} 
                     for x in attributes_options],
            value=attributes_options[:2],
            multi=True
        ),
        dcc.Graph(id="splom"),
])

@app.callback(
    Output("splom", "figure"), 
    [Input("dropdown", "value")])
def update_bar_chart(dims):
    fig = px.scatter_matrix(
        df, dimensions=dims, color="species")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
