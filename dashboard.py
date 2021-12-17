#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import numpy as np
import matplotlib.image as mpimg
import seaborn as sns

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

# # Attributes
# attributes = ff_data.columns.values
# attributes_options = [{'label': i, 'value': i} for i in attributes]


### Dashboard ###

app = dash.Dash(__name__)
app.title = "Forest fires in Montesinho Park"

app.layout = html.Div([
    html.Div(className="wrapper", children=[
        html.H1(id="myheadline", children="Forest fires in Montesinho",
                style={'textAlign': 'center'})
    ]),
    
    html.Div([
    dcc.Graph(id='heatmap'),
    dcc.Graph(id='timeline')
    ])
])
    

# Funktioner - Heatmap
@app.callback(
    Output('heatmap', 'figure'),
    Input('month', 'value'))

def update_heatmap(selected_month):
    fire = ff_data
    fire['ln(area+1)']=np.log(fire['area']+1)
    filtered_df = fire[fire.month == selected_month]

    count = filtered_df.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)
    fires=count.pivot_table(index='Y', columns='X', values='fires')
    my_image = mpimg.imread("./forestfires.jpg")
    heatmap = sns.heatmap(fires, alpha=0.7, zorder=3) 
    heatmap.imshow(my_image,
             aspect=heatmap.get_aspect(),
             extent= heatmap.get_xlim() + heatmap.get_ylim(),
             zorder=1)
    
    return heatmap

@app.callback(
    Output('histogram', 'figure'),
    Input('histogram', 'value'))

def histogram():
    histo = px.histogram(
        ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                        "may", "jun", "jul", "aug",
                                                        "sep", "oct", "nov", "dec"]),
        range_y=[0,200]
    )
    histo.update_xaxes(title_text='Month')
    histo.update_yaxes(title_text='')

    return histo


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)

# def update_output(month):
#     fire = ff_data
#     fire['ln(area+1)']=np.log(fire['area']+1)
#     count = fire.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)
#     fires=count.pivot_table(index='Y', columns='X', values='fires')
#     my_image = mpimg.imread("./forestfires.jpg")
#     heatmap = sns.heatmap(fires, alpha=0.7, zorder=3) 
#     heatmap.imshow(my_image,
#              aspect=h.get_aspect(),
#              extent= h.get_xlim() + h.get_ylim(),
#              zorder=1)
    
#     return heatmap


# # Statiske figurer
# @app.callback(
#     Output('histogram', 'figure'),
#     Input('month', 'value'))

# def output():
#     histo = px.histogram(
#         ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
#                                                         "may", "jun", "jul", "aug",
#                                                         "sep", "oct", "nov", "dec"]),
#         range_y=[0,200]
#     )
#     fig.update_xaxes(title_text='Month')
#     fig.update_yaxes(title_text='')
    
#     return histo
# )














#%% Forsøg med inspiration fra Uber Data App

import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px

import dash_html_components as html

from plotly import graph_objs as go
from plotly.graph_objs import *

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

app = dash.Dash(__name__)

app.title = "Forest fires in Montesinho Park"
server = app.server

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("Forest fires in Montesinho Park"),
                        html.P(
                            """Select different months by selecting
                            different months on the histogram."""
                        ),
                        # html.Div(
                        #     className="div-for-dropdown",
                        #     children=[
                        #         "Month",
                        #         dcc.Dropdown(
                        #             id='month',
                        #             options=[
                        #                 {'label': 'Jan', 'value': 'jan'},
                        #                 {'label': 'Feb', 'value': 'feb'},
                        #                 {'label': 'all', 'value': 'all'}
                        #             ],
                        #             value='all',
                        #         )
                        #     ]),
                                
                        # html.P(id="total-fires"),
                        # html.P(id="total-fires-selection"),
                        # html.P(id="month-value"),
                       
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Select any of the bars on the histogram to section data by month."
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

# Get the amount of fires per month based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(month, day, selection):
    xVal = []
    yVal = []
    xSelected = []

   

    

### DENNE DEL SKAL KIGGES PÅ
# Selected Data in the Histogram updates the Values in the Hours selection dropdown menu
@app.callback(
    Output("bar-selector", "value"),
    [Input("histogram", "selectedData"), Input("histogram", "clickData")],
)

def update_bar_selector(value, clickData):
    holder = []
    if clickData:
        holder.append(str(int(clickData["points"][0]["x"])))
    if value:
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))





# Update Histogram Figure based on Month
@app.callback(
    Output("histogram", "figure"),
    [Input("bar-selector", "value")],
)
def update_histogram():
    histogram = px.histogram(
        ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                        "may", "jun", "jul", "aug",
                                                        "sep", "oct", "nov", "dec"]),
        range_y=[0,200]
    )
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='')
    return histogram


# Update Map Graph based on month-picker, selected data on histogram
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("bar-selector", "value"),
    ],
)
def update_heatmap():
    fire = ff_data
    fire['ln(area+1)']=np.log(fire['area']+1)
    count = fire.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)
    fires=count.pivot_table(index='Y', columns='X', values='fires')
    my_image = mpimg.imread("./forestfires.jpg")
    h = sns.heatmap(fires, alpha=0.7, zorder=3) 
    h.imshow(my_image,
             aspect=h.get_aspect(),
             extent= h.get_xlim() + h.get_ylim(),
             zorder=1)
    return h





if __name__ == '__main__':
    app.run_server(debug=True, port=8080)