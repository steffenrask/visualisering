#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go


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
# Hjælpefunktioner

img = Image.open("forestfires.jpg")
#create an empty dataset with one entry for each cell on the map

emptyMap = []

for y in range(1, 10):

    for x in range(1, 10):

        emptyMap.append({"X": x, "Y": y, "fires": 0})

emptyFrame = pd.DataFrame(emptyMap) #convert the array to a pandass dataframe



###### Figurer om vejret #######

month = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]

# Temperatur
temperature = [4.5, 6.2, 9.2, 10.7, 14, 18.8, 21.7, 21.6, 18.4, 13.2, 8.2, 5.4]

# Avg high/low temp
h_temp = [8.3, 9.4, 12.6, 15.5, 19.6, 23.8, 28.2, 28.3, 24.3, 18.3, 11, 8.9]
l_temp = [1.3, 1.2, 2.7, 4.6, 8, 11.2, 13.8, 13.4, 11.5, 8.6, 4.3, 2]

# Add
#days_with_rain = [10, 9, 6, 9, 10, 5, 3, 3, 5, 9, 9, 11]

# Fra WA
days_with_rain = [14.3, 11.6, 15.7, 17.6, 14.3, 10, 5.8, 4.2, 7.2, 12.5, 15.8, 12.7]
# Wind (https://www.weather-atlas.com/en/portugal/braganca-climate#wind)
wind = [9.7, 10.9, 11.2, 9.9, 9.4, 9.3, 8.9, 9, 8.4, 8.6, 10.3, 8.8]

# Air humidity (https://www.weather-atlas.com/en/portugal/braganca-climate#humidity_relative)
humidity = [85, 81, 76, 75, 69, 63, 55, 52, 57, 70, 83, 84]

# Figure
weather = go.Figure()

weather.add_trace(go.Scatter(
    x=month,
    y=h_temp,
    name="High temp",
    yaxis="y",
    line=dict(color='royalblue')
))

weather.add_trace(go.Scatter(
    x=month,
    y=l_temp,
    name="Low temp",
    yaxis="y",
    line=dict(color='firebrick')
))

weather.add_trace(go.Scatter(
    x=month,
    y=days_with_rain,
    name="Rain",
    yaxis="y"
))

weather.add_trace(go.Scatter(
    x=month,
    y=wind,
    name="Wind",
    yaxis="y"
))

weather.add_trace(go.Scatter(
    x=month,
    y=humidity,
    name="RH",
    yaxis="y2",
    line=dict(dash='dot')
))

weather.update_layout(
    yaxis=dict(
        title="Y",
        range=[0,30]
    ),
    yaxis2=dict(
        title="RH",
        overlaying="y",
        side="right",
        position=0.95,
        range=[0,100]
    ),
    hovermode="x unified",
            hoverlabel=dict(
              bgcolor="white",
              font_size=16,
              font_family="Rockwell")
)    

###### Figurer om sammenhænge mellem vejr og fires #######

#temp
data=ff_data
w = ["temp", "RH", "rain", "wind"]
weather_options = [{'label': i.capitalize(), 'value': i} for i in w]

deg_index = [0,5,10,15,20,25,30,35]
x_deg = [5,10,15,20,25,30,35]

deg = pd.cut(data["temp"], bins=deg_index, labels=x_deg)

count_deg = deg.groupby(deg).count()

y_deg = []

for i in range(len(count_deg)):
    y_deg.append(count_deg[i])

fig1 = px.bar(x=x_deg, y=y_deg, labels={'x':'Temperature', 'y':'Number of fires'})

fig1.update_traces(width=3)
fig1.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"))

# air humidity 
rh_index = [0,10,20,30,40,50,60,70,80,90,100,110]
x_rh = [10,20,30,40,50,60,70,80,90,100,110]

rh = pd.cut(data["RH"], bins=rh_index, labels=x_rh)

count_rh = rh.groupby(rh).count()

y_rh = []

for i in range(len(count_rh)):
    y_rh.append(count_rh[i])

fig2 = px.bar(x=x_rh, y=y_rh, labels={'x':'RH', 'y':'Number of fires'})

fig2.update_traces(width=5)
fig2.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"))

# rain

rain_index = [-1,0.1,0.2,0.3,0.4,0.5]
x_rain = [0,0.1,0.2,0.3,0.4]

rain = pd.cut(data["rain"], bins=rain_index, labels=x_rain)

count_rain = rain.groupby(rain).count()

y_rain = []

for i in range(len(count_rain)):
    y_rain.append(count_rain[i])
  
fig6 = px.bar(x=x_rain, y=y_rain, labels={'x':'Rain', 'y':'Number of fires'})

fig6.update_traces(width=0.08)
fig6.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"))

# wind
wind_index = [-1,0,1,2,3,4,5,6,7,8,9,10,11]
x_wind = [0,1,2,3,4,5,6,7,8,9,10,11]

wind = pd.cut(data["wind"], bins=wind_index, labels=x_wind)

count_wind = wind.groupby(wind).count()

y_wind = []

for i in range(len(count_wind)):
    y_wind.append(count_wind[i])
    
fig4 = px.bar(x=x_wind, y=y_wind, labels={'x':'Wind', 'y':'Number of fires'})

fig4.update_traces(width=0.5)
fig4.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"))

# Dash Layout
app.layout = html.Div([
                 html.H1(children="Forest fires in Montesinho Natural Park",
                         style = {'textAlign':'center', 'font-family' : 'Roboto'}),   
                 
                 html.Div(
                     className="text-padding",
                        children=[
                            "An overview of forest fires in Montesinho Natural Park from January 2000 to December 2003."
                        ], style={'width':'96%','vertical-align':'top','margin':'2%'}
                        ),
                 
                 dcc.Markdown(
                     """
                     Sources: [UCI](https://archive.ics.uci.edu/ml/datasets/forest+fires), 
                     [WeatherAtlas](https://www.weather-atlas.com/en/portugal/braganca-climate)
                     """,
                     style={'vertical-align':'top','margin':'2%'}
                     ),
                     
                 html.P(id="total-fires",
                          style={'vertical-align':'top','margin':'2%'}
                        ),
                 html.P(id="total-fires-selection",
                          style={'vertical-align':'top','margin':'2%'}
                        ),
                 
                 html.Div(
                            className="text-padding",
                            children=[
                                "Select month:"
                            ],
                            style={'vertical-align':'top','margin':'2%'}
                        ),
                 
                 html.Div([
                     dcc.RadioItems(id='selections',
                          options=month_options,
                          value='all',
                          style={'width':'95%','vertical-align':'top','margin':'2%'}
                          #style={'display':'flex'}
                          )
                ]),
                
                 
                 html.Div([
                     dcc.Graph(id='heat-map',
                               style={'width':'95%','vertical-align':'top','margin':'2%'})
                     ]),
                 
                 html.Div(
                            className="text-padding",
                            children=[
                                "Select month on the histogram to section data in heatmap by month:"
                            ], 
                            style={'width':'95%','vertical-align':'top','margin':'2%'}
                        ),
                 
                 html.Div([
                     dcc.Graph(id='histogram',
                               style={'width':'95%','vertical-align':'top','margin':'2%'},
                               figure=histogram
                               )
                 ]),
                 
                 
                 html.Div([
                      html.Div(
                          className="text-padding",
                          children=[
                              """Average weather in Montesinho Natural Park during the year.
                                     Average temperatures (Temp), average number
                                     of days with rain (Rain), average wind speed (Wind), and 
                                     average relative humidity (RH):"""],
                          style={'width': '46%', 'display': 'inline-block', 'margin': '2%'}),
                   
                     html.Div([
                         dcc.RadioItems(id='selection_1',
                                        options=weather_options,
                                        value='temp',
                                        style={'display':'flex'})
                     ], style={'width': '46%', 'display': 'inline-block', 'margin': '2%'
                     })]),
                           
                 html.Div([
                     html.Div([
                         dcc.Graph(id='weather',
                                   figure=weather)
                     ], style={'width': '46%', 'display': 'inline-block', 'margin': '2%'
                     }),
                               
                     html.Div([
                         dcc.Graph(id='bar_chart_1',
                                   )
                     ], style={'width': '46%', 'display': 'inline-block', 'margin': '2%'
                     })])
                             
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


@app.callback(
    Output(component_id="bar_chart_1", component_property='figure'),
    Input(component_id='selection_1', component_property='value')
)

def update_output_1(weather_option):
    #bar_chart_1 = fig1
    
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

if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
    









    
    
    