#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 15:49:31 2021

@author: steffenrask
"""

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

#%% First try:

# Tidslinje med måneder og count på fires

fig = px.histogram(
    ff_data, x="month", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                    "may", "jun", "jul", "aug",
                                                    "sep", "oct", "nov", "dec"]),
    range_y=[0,200]
)
fig.update_xaxes(title_text='Month')
fig.update_yaxes(title_text='')
fig.show(renderer="chrome")


# Tidslinje med dage og count på fires

fig = px.histogram(
    ff_data, x="day", category_orders=dict(day=["mon", "tue", "wed", "thu",
                                                     "fri", "sat", "sun"]),
range_y=[0,100]
)
fig.update_xaxes(title_text='Day')
fig.update_yaxes(title_text='')
fig.show(renderer="chrome")


# Kombineret tidslinje:

fig = px.histogram(
    ff_data, x="day", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                    "may", "jun", "jul", "aug",
                                                    "sep", "oct", "nov", "dec"],
                                             day=["mon", "tue", "wed", "thu",
                                                  "fri", "sat", "sun"]),
    facet_col = "month", facet_col_spacing=0.001
    
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='')

fig.show(renderer="chrome")


# MANGLER: Hover-funktion

#%%
# Take 2 med area burned i stedet for counts

fig2 = px.histogram(
    ff_data, x="day", category_orders=dict(month=["jan", "feb", "mar", "apr",
                                                    "may", "jun", "jul", "aug",
                                                    "sep", "oct", "nov", "dec"],
                                             day=["mon", "tue", "wed", "thu",
                                                  "fri", "sat", "sun"]),
    y="area",
    facet_col = "month", facet_col_spacing=0.001
)
fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig2.update_xaxes(title_text='')
fig2.update_yaxes(title_text='')

fig2.show(renderer="chrome")

#%% Så kombineres med go

fig3 = fig3 = go.Figure(data=fig.data + fig2.data)
fig3.show(renderer="chrome")

# TEST TEST

