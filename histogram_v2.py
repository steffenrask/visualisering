import pandas as pd
import plotly.express as px
# path = "C:/Users/Ribert/OneDrive/Kandidat/3 semester/DS808 Visualisering/Exam/"
data = pd.read_csv('forestfires.csv', encoding='utf-8')


print(data)
print(min(data["Y"]))


        
#%% temp
deg_index = [0,5,10,15,20,25,30,35]
x_deg = [5,10,15,20,25,30,35]

deg = pd.cut(data["temp"], bins=deg_index, labels=x_deg)

count_deg = deg.groupby(deg).count()

y_deg = []

for i in range(len(count_deg)):
    y_deg.append(count_deg[i])

fig = px.bar(x=x_deg, y=y_deg, labels={'x':'degrees', 'y':'number of fires'})

fig.update_traces(width=3)

fig.show(renderer='browser')




#%% air humidity 
rh_index = [0,10,20,30,40,50,60,70,80,90,100,110]
x_rh = [10,20,30,40,50,60,70,80,90,100,110]

rh = pd.cut(data["RH"], bins=rh_index, labels=x_rh)

count_rh = rh.groupby(rh).count()

y_rh = []

for i in range(len(count_rh)):
    y_rh.append(count_rh[i])

fig = px.bar(x=x_rh, y=y_rh, labels={'x':'RH', 'y':'number of fires'})

fig.update_traces(width=5)

fig.show(renderer='browser')



#%% rain

rain_index = [-1,0.1,0.2,0.3,0.4,0.5]
x_rain = [0,0.1,0.2,0.3,0.4]

rain = pd.cut(data["rain"], bins=rain_index, labels=x_rain)

count_rain = rain.groupby(rain).count()

y_rain = []

for i in range(len(count_rain)):
    y_rain.append(count_rain[i])
  
fig = px.bar(x=x_rain, y=y_rain, labels={'x':'rain', 'y':'number of fires'})

fig.update_traces(width=0.08)

fig.show(renderer='browser')

#%% wind
wind_index = [-1,0,1,2,3,4,5,6,7,8,9,10,11]
x_wind = [0,1,2,3,4,5,6,7,8,9,10,11]

wind = pd.cut(data["wind"], bins=wind_index, labels=x_wind)

count_wind = wind.groupby(wind).count()

y_wind = []

for i in range(len(count_wind)):
    y_wind.append(count_wind[i])
    
fig = px.bar(x=x_wind, y=y_wind, labels={'x':'wind', 'y':'number of fires'})

fig.update_traces(width=0.5)

fig.show(renderer='browser')

#%%

mean_deg = [4.5, 6.2, 9.2, 10.7, 14, 18.8, 21.7, 21.6, 18.4, 13.2, 8.2, 5.4]


month = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]


fig = px.bar(x=month, y=mean_deg, labels={'x':'wind', 'y':'number of fires'})

fig.update_traces(width=0.5)

fig.show(renderer='browser')

#%%

days_with_rain = [10, 9, 6, 9, 10, 5, 3, 3, 5, 9, 9, 11]

month = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]

fig = px.bar(x=month, y=days_with_rain, labels={'x':'wind', 'y':'number of fires'})

fig.update_traces(width=0.5)

fig.show(renderer='browser')