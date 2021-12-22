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
#import numpy as np
#import plotly.graph_objects as go


app = dash.Dash(__name__)
app.title = "Forest fires in Montesinho Natural Park"

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
month_options = [{'label': i.capitalize(), 'value': i} for i in months]
month_options.append({'label': 'All Months', 'value': 'all'})



#### Histogram #####
histogram = px.histogram(
    ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                    "may", "jun", "jul", "aug",
                                                    "sep", "oct", "nov", "dec"]),
    range_y=[0,200]
)
histogram.update_xaxes(title_text='Month')
histogram.update_yaxes(title_text='Forest fires 2000-2003')


##### Heatmap ######

img = Image.open("forestfires.jpg")
#create an empty dataset with one entry for each cell on the map

emptyMap = []

for y in range(1, 10):

    for x in range(1, 10):

        emptyMap.append({"X": x, "Y": y, "fires": 0})

emptyFrame = pd.DataFrame(emptyMap) #convert the array to a pandass dataframe



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
                 
                 html.Div(
                            className="text-padding",
                            children=[
                                "An overview of forest fires in Montesinho Natural Park from January 2000 to December 2003."
                            ],
                        ),
                 
                 html.P(id="total-fires"),
                 html.P(id="total-fires-selection"),
                 
                 html.Div(
                            className="text-padding",
                            children=[
                                "Select month:"
                            ],
                        ),
                 
                 html.Div([
                     dcc.RadioItems(id='selections',
                          options=month_options,
                          value='all',
                          style={'display':'flex'}
                          )
                ]),
                
                 
                 html.Div([
                     dcc.Graph(id='heat-map')
                     ]),
                 
                 html.Div(
                            className="text-padding",
                            children=[
                                "Select month on the histogram to section data in heatmap by month:"
                            ],
                        ),
                 
                 html.Div([
                     dcc.Graph(id='histogram',
                               figure=histogram
                               )
                 ])
])

##### Callbacks

# Selected Data in the Histogram updates the values in the month selection
@app.callback(
    Output("selections", "value"),
    Input("histogram", "clickData"),
)
def update_bar_selector(clickData):
    month_option = 'all'
    if clickData:
        month_option = clickData['points'][0]['x']
    return month_option


# Heatmap med RadioItem             

@app.callback([
      Output(component_id='heat-map', component_property='figure'),
      Output("total-fires", "children"), 
      Output("total-fires-selection", "children")]
      ,
      Input(component_id='selections', component_property='value')
)

def update_output(month_option):
    
    #Pick data for chosen single month(s) or all:
    mydata = ff_data

    #print(selection, flush=True)
    if month_option != 'all':
        mydata = mydata[mydata['month'] == month_option]

    #Heatmap
    count = mydata.groupby(['X', 'Y'], dropna=False).size().reset_index(name='fires').fillna(0)        
    
    merged = pd.concat([emptyFrame, count], axis=0, join='inner') #merge both dataframes on their shared columns
    
    fires=merged.pivot_table(index='Y', columns='X', values='fires')
    fires=fires*2
    
    # print(count, flush=True)
    # print(merged, flush=True)
    # print(fires, flush=True)

    fig = px.imshow(fires, aspect='auto', color_continuous_scale=[(0, "rgba(0, 0, 0, 0)"), (1, "red")])
    fig.update_yaxes(fixedrange=True, range=(1, 9.5), dtick=1, showgrid=False)
    fig.update_xaxes(fixedrange=True, range=(0.5, 9.5), dtick=1, showgrid=False)
    fig.add_layout_image(
            dict(
                source=img,
                xref='x domain',
                yref='y domain',
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                layer="below")
            )
    
    
    #Update counters
    total = "Total fires in dataset: "+str(len(ff_data))
    total_sel = "Total fires in selection: "+str(len(mydata))
    
    return fig, total, total_sel
    



if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
    









    
    
    