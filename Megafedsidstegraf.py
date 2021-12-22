# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 20:06:05 2021

@author: 45414
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
histogram.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"))

##### Heatmap ######

img = Image.open("forestfires.jpg")
#create an empty dataset with one entry for each cell on the map

emptyMap = []

for y in range(1, 10):

    for x in range(1, 10):

        emptyMap.append({"X": x, "Y": y, "fires": 0})

emptyFrame = pd.DataFrame(emptyMap) #convert the array to a pandass dataframe
#%%
#### Barcharts #####
#### Barcharts #####
#%% temp
data=ff_data
weather = ["temp", "RH", "rain", "wind"]
weather_options = [{'label': i.capitalize(), 'value': i} for i in weather]

deg_index = [0,5,10,15,20,25,30,35]
x_deg = [5,10,15,20,25,30,35]

deg = pd.cut(data["temp"], bins=deg_index, labels=x_deg)

count_deg = deg.groupby(deg).count()

y_deg = []

for i in range(len(count_deg)):
    y_deg.append(count_deg[i])

fig1 = px.bar(x=x_deg, y=y_deg, labels={'x':'Temperature', 'y':'Number of fires'})

fig1.update_traces(width=3)





#%% air humidity 
rh_index = [0,10,20,30,40,50,60,70,80,90,100,110]
x_rh = [10,20,30,40,50,60,70,80,90,100,110]

rh = pd.cut(data["RH"], bins=rh_index, labels=x_rh)

count_rh = rh.groupby(rh).count()

y_rh = []

for i in range(len(count_rh)):
    y_rh.append(count_rh[i])

fig2 = px.bar(x=x_rh, y=y_rh, labels={'x':'RH', 'y':'Number of fires'})

fig2.update_traces(width=5)




#%% rain

rain_index = [-1,0.1,0.2,0.3,0.4,0.5]
x_rain = [0,0.1,0.2,0.3,0.4]

rain = pd.cut(data["rain"], bins=rain_index, labels=x_rain)

count_rain = rain.groupby(rain).count()

y_rain = []

for i in range(len(count_rain)):
    y_rain.append(count_rain[i])
  
fig6 = px.bar(x=x_rain, y=y_rain, labels={'x':'Rain', 'y':'Number of fires'})

fig6.update_traces(width=0.08)


#%% wind
wind_index = [-1,0,1,2,3,4,5,6,7,8,9,10,11]
x_wind = [0,1,2,3,4,5,6,7,8,9,10,11]

wind = pd.cut(data["wind"], bins=wind_index, labels=x_wind)

count_wind = wind.groupby(wind).count()

y_wind = []

for i in range(len(count_wind)):
    y_wind.append(count_wind[i])
    
fig4 = px.bar(x=x_wind, y=y_wind, labels={'x':'Wind', 'y':'Number of fires'})

fig4.update_traces(width=0.5)


#%%

mean_deg = [4.5, 6.2, 9.2, 10.7, 14, 18.8, 21.7, 21.6, 18.4, 13.2, 8.2, 5.4]


month = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]


fig5 = px.bar(x=month, y=mean_deg, labels={'x':'Month', 'y':'Mean_deg'})

fig5.update_traces(width=0.5)


#%%

days_with_rain = [10, 9, 6, 9, 10, 5, 3, 3, 5, 9, 9, 11]

month = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]

fig3 = px.bar(x=month, y=days_with_rain, labels={'x':'Month', 'y':'Days_with_rain'})

fig3.update_traces(width=0.5)

bar_chart = px.histogram(
    ff_data, x=["temp",'RH','rain','wind'], category_orders=dict(month=['Temperature', 'RH', 'Rain','Wind']),
    range_y=[0,200]
    )

#%%

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
                 ]),
                 html.Div([
                   html.Div([
                     dcc.RadioItems(id='selection_1',
                                    options=weather_options,
                                    value='all',
                                    style={'display':'flex'})
                 ], style={'width': '46%', 'display': 'inline-block', 'margin': '2%'
                     }),
                 html.Div([
                     dcc.RadioItems(id='selection_2',
                                    options=weather_options,
                                    value='all',
                                    style={'display':'flex'})
                 ], style={'width': '46%', 'display': 'inline-block', 'margin': '2%'
                 })]),
                 html.Div([
                     html.Div([
                         dcc.Graph(id='bar_chart_1',
                                   )
                     ], style={'width': '46%', 'display': 'inline-block', 'margin': '2%'
                     }),
                     html.Div([
                         dcc.Graph(id='bar_chart_2',
                                   )
                     ], style={'width': '46%', 'display': 'inline-block', 'margin': '2%'
                     })])
])

##### Callbacks ######

@app.callback(
    Output(component_id="bar_chart_1", component_property='figure'),
    Input(component_id='selection_1', component_property='value')
)

def update_output_1(weather_option):
        if weather_option == 'temp':
            bar_chart_1 = fig1
        if weather_option == 'RH':
            bar_chart_1 = fig2
        if weather_option == 'rain':
            bar_chart_1 = fig6
        if weather_option == 'wind':
            bar_chart_1 = fig4
        bar_chart_1.update_yaxes(fixedrange=True)
        return bar_chart_1
@app.callback(
    Output(component_id="bar_chart_2", component_property='figure'),
    Input(component_id='selection_2', component_property='value')
)
def update_output_2(weather_option):
        if weather_option == 'temp':
            bar_chart_2 = fig1
        if weather_option == 'RH':
            bar_chart_2 = fig2
        if weather_option == 'rain':
            bar_chart_2 = fig6
        if weather_option == 'wind':
            bar_chart_2 = fig4
        
        bar_chart_2.update_yaxes(fixedrange=True)
        return bar_chart_2

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
    fig.update_traces(hovertemplate= 'X-value: %{x}<br>'+'Y-value: %{y}<br>' + 'Fires: %{z}'+"<extra></extra>")
    fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"))
    
    #Update counters
    total = "Total fires in dataset: "+str(len(ff_data))
    total_sel = "Total fires in selection: "+str(len(mydata))
    
    return fig, total, total_sel
    



if __name__ == '__main__':
    app.run_server(debug=False, port=8081)
    