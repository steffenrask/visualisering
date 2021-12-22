#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 17:01:26 2021

@author: steffenrask

Dash simpel med checklist for måneder

Inspireret af volcanos

"""

import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
from PIL import Image
import numpy as np
#import plotly.graph_objects as go


app = dash.Dash(__name__)
app.title = "Forest fires in Montesinho Park"

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
month_options = [{'label': i, 'value': i} for i in months]
month_options.append({'label': 'All Months', 'value': 'all'})

# Lav liste med lister for hver måned
totalList = []
monthlyList = []

for month in months:
    monthlyList = ff_data.loc[ff_data['month'] == month]
    totalList.append(monthlyList)
totalList = np.array(totalList, dtype=object)

# Histogram
histogram = px.histogram(
    ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                    "may", "jun", "jul", "aug",
                                                    "sep", "oct", "nov", "dec"]),
    range_y=[0,200]
)
histogram.update_xaxes(title_text='Month')
histogram.update_yaxes(title_text='Fires')


# Olivers figurer

#
#
#
#
#
#


# Dash Layout
app.layout = html.Div([
                 html.H1(children="Forest fires in Montesinho Park",
                         style = {'textAlign':'center', 'font-family' : 'Roboto'}),        
                 
                 html.Div([
                     dcc.RadioItems(id='selections',
                         options=month_options,
                         value='all',
                         style={'width':'50%','display':'inline-block'})
                ]),
                 
                 html.Div([
                     dcc.Graph(id='heat-map')
                     ]),
                 html.Div([
                     dcc.Graph(id='histogram',
                               figure=histogram
                               )
                 ])
])



# Callbacks                

@app.callback(
      Output(component_id='heat-map', component_property='figure')
      ,
      Input(component_id='selections', component_property='value')
)

def update_output(selection):
    
    #Pick data for chosen single month(s) or all:
    mydata = ff_data
    
    #print(selection, flush=True)
    if selection != 'all':
        mydata = mydata[mydata['month'] == selection]

    #Heatmap
    count = mydata.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)        
    fires=count.pivot_table(index='Y', columns='X', values='fires')
    img = Image.open("forestfires.jpg")

    fig = px.imshow(fires, aspect='auto', color_continuous_scale=[(0, "rgba(0, 0, 0, 0)"), (1, "red")])
    fig.update_yaxes(type="linear", fixedrange=True, range=(0.5, 9.5))
    fig.update_xaxes(type="linear", fixedrange=True, range=(0.5, 9.5))
    fig.add_layout_image(
            dict(
                source=img,
                #xref='x domain',
                #yref='y domain',
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                layer="below")
            )
    
    return fig
    

##### Her clickdata

if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
    









    
    
    