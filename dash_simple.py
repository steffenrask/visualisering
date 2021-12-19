#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 17:01:26 2021

@author: steffenrask

Dash simpel med slider for tid - så vi har en backup

Inspireret af volcanos

"""

import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import matplotlib.image as mpimg
import seaborn as sns

app = dash.Dash(__name__)
app.title = "Forest fires in Montesinho Park"

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

time = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

app.layout = html.Div([
                 html.H1(children="Forest fires in Montesinho Park - Simple",
                         style = {'textAlign':'center', 'font-family' : 'Roboto'}),        
                 
                 html.Div([
                     html.Div(
                         className="visrow",
                         children=[
                             dcc.Graph(id='heatmap')
                         ]),
                     html.Div(
                         className="visrow",
                         children=[
                             dcc.Graph(id='histogram')
                         ]),
                 ]),
                 
                 html.Div([
                     dcc.Slider(
                       id='time-slider',
                       min='all',
                       max='dec',
                       step=None,
                       value=13,
                       marks={
                           'all': "All",
                           'jan': "January",
                           'feb': "February",
                           'mar': "March",
                           'apr': "April",
                           'may': "May",
                           'jun': "June",
                           'jul': "July",
                           'aug': "August",
                           'sep': "September",
                           'oct': "October",
                           'nov': "November",
                           'dec': "December"}
                           )
                 ])
])
                 

@app.callback([
     Output(component_id='heatmap', component_property='figure'),
     Output(component_id='histogram', component_property='figure')
     ],
    [
#     Input(component_id='histogram', component_property='value'),
     Input(component_id='time-slider', component_property='value')
    ]
)

def update_output(selected_month):
    mydata = ff_data
    if selected_month != 'all':
        mydata = ff_data[ff_data['month'] == selected_month]
    
    count = mydata.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)
    fires=count.pivot_table(index='Y', columns='X', values='fires')
    my_image = mpimg.imread("./forestfires.jpg")
    heatmap = sns.heatmap(fires, alpha=0.7, zorder=3)
    heatmap.imshow(my_image,
             aspect=heatmap.get_aspect(),
             extent= heatmap.get_xlim() + heatmap.get_ylim(),
             zorder=1)

    histogram = px.histogram(
        mydata, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                        "may", "jun", "jul", "aug",
                                                        "sep", "oct", "nov", "dec"]),
        range_y=[0,200]
    )
    histogram.update_xaxes(title_text='Month')
    histogram.update_yaxes(title_text='')


    return heatmap, histogram

if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
    
    
    
    
    
    