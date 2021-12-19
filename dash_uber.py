#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 16:05:02 2021

@author: steffenrask

Dashboard inspireret af Dash Uber APP
https://dash.gallery/dash-uber-rides-demo/
https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-uber-rides-demo/app.py

"""


import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import matplotlib.image as mpimg
import seaborn as sns
from plotly import graph_objs as go
#from plotly.graph_objs import *
import numpy as np

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')
asd = pd.to_datetime(ff_data['month'], format='%b').dt.month
ff_data['asd'] = asd

totalList = []
for month in ff_data.groupby('month'):
    totalList.append(month[1])
totalList = np.array(totalList)





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
                            """Select different months in the dropdown or on the histogram."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="bar-selector",
                                    options=[
                                        {
                                            "label": str(n),
                                            "value": str(n),
                                            }
                                        for n in ["jan", "feb", "mar", "apr",
                                                  "may", "jun", "jul", "aug",
                                                  "sep", "oct", "nov", "dec"]
                                        ],
                                    multi=True,
                                    placeholder="Select month",
                                )
                            ]),
                        html.P(id="total-fires-selection")
                        ],
                    
                    ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="heatmap"),
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
def get_selection(month, selection):
     xVal = []
     yVal = []
     xSelected = []
     colorVal = []
     
     # Put selected months into a list of numbers xSelected
     xSelected.extend([int(x) for x in selection])

     for i in range(12):
         # If bar is selected then color it white
         if i in xSelected and len(xSelected) < 12:
             colorVal[i] = "#FFFFFF"
         xVal.append(i)
         # Get the number of fires at a particular month
         yVal.append(len(totalList.index.month == i))
     return [np.array(xVal), np.array(yVal)]




# Selected Data in the Histogram updates the Values in the Month selection dropdown menu
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


# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    if clickData:
        return {"points": []}



# Update the total number of fires in selected months
@app.callback(
    [Output("total-fires-selection", "children")],
    [Input("bar-selector", "value")],
)
def update_total_fires_selection(monthPicked, selection):
    firstOutput = ""

    if selection != None or len(selection) != 0:
        #month_picked = bar-selector
        totalInSelection = 0
        for x in selection:
            totalInSelection += len(
                totalList[month][
                    totalList.index.month
                    == int(x)
                ]
            )
        firstOutput = "Total rides in selection: {:,d}".format(totalInSelection)

    if (
        monthPicked is None
        or selection is None
        or len(selection) == 12
        or len(selection) == 0
    ):
        return firstOutput, (monthPicked, " - showing month(s): All")

    holder = sorted([int(x) for x in selection])

    if holder == list(range(min(holder), max(holder) + 1)):
        return (
            firstOutput,
            (
                monthPicked,
                " - showing month(s): ",
                holder[0],
                "-",
                holder[len(holder) - 1],
            ),
        )

    holder_to_string = ", ".join(str(x) for x in holder)
    return firstOutput, (monthPicked, " - showing month(s): ", holder_to_string)






# Update Histogram Figure based on Month chosen
@app.callback(
    Output("histogram", "figure"),
    Input("bar-selector", "value"),
)
def update_histogram(monthPicked, selection):
    [xVal, yVal, colorVal] = get_selection(monthPicked, selection)

    # layout = go.Layout(
    #     bargap=0.01,
    #     bargroupgap=0,
    #     barmode="group",
    #     margin=go.layout.Margin(l=10, r=0, t=0, b=50),
    #     showlegend=False,
    #     plot_bgcolor="#323130",
    #     paper_bgcolor="#323130",
    #     dragmode="select",
    #     font=dict(color="white"),
    #     xaxis=dict(
    #         range=[-0.5, 11.5],
    #         showgrid=False,
    #         nticks=13,
    #         fixedrange=True
    #     ),
    #     yaxis=dict(
    #         range=[0, max(yVal) + max(yVal) / 4],
    #         showticklabels=False,
    #         showgrid=False,
    #         fixedrange=True,
    #         rangemode="nonnegative",
    #         zeroline=False,
    #     ),
    #     annotations=[
    #         dict(
    #             x=xi,
    #             y=yi,
    #             text=str(yi),
    #             xanchor="center",
    #             yanchor="bottom",
    #             showarrow=False,
    #             font=dict(color="white"),
    #         )
    #         for xi, yi in zip(xVal, yVal)
    #     ],
    # )
    
    histogram = px.histogram(
        ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                        "may", "jun", "jul", "aug",
                                                        "sep", "oct", "nov", "dec"]),
        range_y=[0,200]
    )
    histogram.update_xaxes(title_text='Month')
    histogram.update_yaxes(title_text='')
    
    
    
    # return go.Figure(
    #     data=[
    #         go.Histogram(x=xVal, marker=dict(color=colorVal), hoverinfo="x")
    #         histogram.update_xaxes(categoryorder='array', categoryarray= 
    #                                ["jan", "feb", "mar", "apr", "may", "jun",
    #                                 "jul", "aug", "sep", "oct", "nov", "dec"])
    #         histogram.update_xaxes(title_text='Month')
    #         histogram.update_yaxes(title_text='')],
    #     layout=layout,
    # )



# # Update Map Graph based on month-picker, selected data on histogram
@app.callback(
    Output("heatmap", "figure"),
    [
        Input("bar-selector", "value")
    ],
)

def update_heatmap(month):

    count = ff_data.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)
    fires=count.pivot_table(index='Y', columns='X', values='fires')
    my_image = mpimg.imread("./forestfires.jpg")    
    heatmap = sns.heatmap(fires, alpha=0.7, zorder=3) # update
    heatmap.imshow(my_image,
             aspect=heatmap.get_aspect(),
             extent= heatmap.get_xlim() + heatmap.get_ylim(),
             zorder=1)
    
    return heatmap




if __name__ == '__main__':
    app.run_server(debug=True, port=8082)
