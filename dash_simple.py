#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 17:01:26 2021

@author: steffenrask

Dash simpel med dropdown for måneder

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

# month_options = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
# month_options.append("all")

month_options = [
    {'label': 'January', 'value': 'jan'},
    {'label': 'February', 'value': 'feb'},
    {'label': 'March', 'value': 'mar'},
    {'label': 'April', 'value': 'apr'},
    {'label': 'May', 'value': 'may'},
    {'label': 'June', 'value': 'jun'},
    {'label': 'July', 'value': 'jul'},
    {'label': 'August', 'value': 'aug'},
    {'label': 'September', 'value': 'sep'},
    {'label': 'October', 'value': 'oct'},
    {'label': 'November', 'value': 'nov'},
    {'label': 'December', 'value': 'dec'}]
month_options.append({'label': 'All Months', 'value': 'all'})


app.layout = html.Div([
                 html.H1(children="Forest fires in Montesinho Park - Simple",
                         style = {'textAlign':'center', 'font-family' : 'Roboto'}),        
                 
                 html.Div([
                     dcc.Checklist(id='checklist',
                         options=month_options,
                         value=['all'])
                ]),
                 
                 # html.Div([
                 #     html.Div(
                 #         className="visrow",
                 #         children=[
                 #             dcc.Graph(id='heatmap')
                 #         ]),
                 html.Div([
                     dcc.Graph(id='histogram')
                 ]),
                 # ])
])
                 

@app.callback([
     #Output(component_id='heatmap', component_property='figure'),
     Output(component_id='histogram', component_property='figure')
     ],
    [
     Input(component_id='checklist', component_property='value')
    ]
)

def update_output(month_option):
    
    # Pick data for single month
    # mydata = ff_data
    # if month_option != 'all':
    #     mydata = ff_data.loc[ff_data['month'] == month_option]
    
    # Heatmap
    # count = mydata.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)
    # fires=count.pivot_table(index='Y', columns='X', values='fires')
    # my_image = mpimg.imread("./forestfires.jpg")
    # heatmap = sns.heatmap(fires, alpha=0.7, zorder=3)
    # heatmap.imshow(my_image,
    #          aspect=heatmap.get_aspect(),
    #          extent= heatmap.get_xlim() + heatmap.get_ylim(),
    #          zorder=1)

    # Histogram
    histogram = px.histogram(
        ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                        "may", "jun", "jul", "aug",
                                                        "sep", "oct", "nov", "dec"]),
        range_y=[0,200]
    )
    histogram.update_xaxes(title_text='Month')
    histogram.update_yaxes(title_text='Fires')


    return histogram


# Her clickdata

if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
    
    
    
    
    
    