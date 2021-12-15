import pandas as pd
import seaborn as sns
import matplotlib.image as mpimg # add
import numpy as np
import matplotlib.pyplot as plt

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

plt.show(renderer='browser') # add
