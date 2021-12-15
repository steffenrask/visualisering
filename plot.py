# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 16:41:47 2021

@author: Ribert
"""

import pandas as pd
import matplotlib.pyplot as plt


path = "C:/Users/Ribert/OneDrive/Kandidat/3 semester/DS808 Visualisering/Exam/"
data = pd.read_csv(path + "forestfires.csv")


print(data)


        
#%% temp
deg_index = [0,5,10,15,20,25,30,35]
x_deg = [5,10,15,20,25,30,35]

deg = pd.cut(data["temp"], bins=deg_index, labels=x_deg)

count_deg = deg.groupby(deg).count()

y_deg = []

for i in range(len(count_deg)):
    y_deg.append(count_deg[i])



plt.bar(x_deg,y_deg, width=3)
plt.ylabel('number of fires')
plt.xlabel('degrees')
plt.show()


#%% air humidity 
rh_index = [0,10,20,30,40,50,60,70,80,90,100,110]
x_rh = [10,20,30,40,50,60,70,80,90,100,110]

rh = pd.cut(data["RH"], bins=rh_index, labels=x_rh)

count_rh = rh.groupby(rh).count()

y_rh = []

for i in range(len(count_rh)):
    y_rh.append(count_rh[i])



plt.bar(x_rh,y_rh, width=5)
plt.ylabel('number of fires')
plt.xlabel('RH')
plt.show()



#%% rain

rain_index = [-1,0.1,0.2,0.3,0.4,0.5]
x_rain = [0,0.1,0.2,0.3,0.4]

rain = pd.cut(data["rain"], bins=rain_index, labels=x_rain)

count_rain = rain.groupby(rain).count()

y_rain = []

for i in range(len(count_rain)):
    y_rain.append(count_rain[i])
    
plt.bar(x_rain,y_rain, width=0.08)
plt.ylabel('number of fires')
plt.xlabel('rain')
plt.show()


#%% wind
wind_index = [-1,0,1,2,3,4,5,6,7,8,9,10,11]
x_wind = [0,1,2,3,4,5,6,7,8,9,10,11]

wind = pd.cut(data["wind"], bins=wind_index, labels=x_wind)

count_wind = wind.groupby(wind).count()

y_wind = []

for i in range(len(count_wind)):
    y_wind.append(count_wind[i])

plt.bar(x_wind,y_wind, width=0.5)
plt.ylabel('number of fires')
plt.xlabel('wind')
plt.show()










