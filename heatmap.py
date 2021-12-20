#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.image as mpimg # add
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html


#%%
fire = pd.read_csv('forestfires.csv', encoding='utf-8')
fire['ln(area+1)']=np.log(fire['area']+1)
df = pd.DataFrame(fire,columns=['X','Y','ln(area+1)'])

#make the df heatmap friendly
pt1=df.pivot_table(index='Y', columns='X', values='ln(area+1)')

#load an image
my_image = mpimg.imread("./forestfires.jpg")

h = sns.heatmap(pt1, alpha=0.7, zorder=3) # update

# update
h.imshow(my_image,
         aspect=h.get_aspect(),
         extent= h.get_xlim() + h.get_ylim(),
         zorder=1)

plt.show(renderer='browser')



#%% 

####### TAKE 2 MED PX OG COUNTS #######

ff_data = pd.read_csv('forestfires.csv', encoding='utf-8')

asd = pd.to_datetime(ff_data['month'], format='%b').dt.month

ff_data['asd'] = asd

# Count
count = ff_data.groupby(['X', 'Y']).size().reset_index(name='fires').fillna(0)

#make the df heatmap friendly
fires=count.pivot_table(index='Y', columns='X', values='fires')

#load an image
my_image = mpimg.imread("./forestfires.jpg")

h = px.imshow(fires)

# update
# h.imshow(my_image,
#          aspect=h.get_aspect(),
#          extent= h.get_xlim() + h.get_ylim(),
#          zorder=1)

h.show(renderer='chrome')
