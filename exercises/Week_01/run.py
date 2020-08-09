import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import imageio
import sys

#### Step 1:
fert = pd.read_csv('data/gapminder_total_fertility.csv', index_col=0)

#### Step 2:
life = pd.read_excel('data/gapminder_lifeexpectancy.xlsx', index_col=0)

#print(fert)
#print(life)

#### Step 3:
#print(life.shape)
#print(fert.shape)

#### Step 4:
ncol = [int(x) for x in fert.columns]
fert.set_axis(axis=1, labels=ncol, inplace=True)

#### Step 5:
sfert = fert.stack()
slife = life.stack()

d = {'fertility': sfert, 'lifeexp': slife}
df2 = pd.DataFrame(data=d)

#### Step 6:
population = pd.read_excel('data/gapminder_population.xlsx', index_col=0)
spop = population.stack()

d = {'fertility': sfert, 'lifeexp': slife, 'population':spop}
df2 = pd.DataFrame(data=d)

#### Step 7:
df3 = df2.stack()
df4 = df3.unstack((0,2))

#### Step 8:
#df4[['Germany', 'France', 'Sweden']].plot()
#plt.show()

df5 = df3.unstack(2)
#df5.plot.scatter('fertility', 'lifeexp', s=0.1)
#plt.show()


df6 = df3.unstack(1)
df6 = df6[1950]
df6 = df6.unstack(1)
#df6.plot.scatter('fertility', 'lifeexp', s=0.1)
#plt.show()


#### Step 9:
#cmap = plt.get_cmap('tab20', lut = len(df6)).colors
#df6.plot.scatter('fertility', 'lifeexp', s=0.1, c=cmap)
#plt.show()
#plt.savefig('images/step_9.png')

#### Step 10:
df7 = df3.unstack(1)

for i in range(1960,2015):
    filename = 'images/lifeexp_'+str(i)+'.png'
    tmp = df7[i]
    tmp = tmp.unstack(1)
    cmap = plt.get_cmap('tab20', lut = len(tmp)).colors
    tmp.plot.scatter('fertility', 'lifeexp', s=tmp['population']/1000000,c=cmap)
    plt.title('Year: '+str(i))
    plt.axis((0,10,0,100))
    plt.savefig(filename)
    plt.close()

#### Step 11:


#### Step 12:
images = []
for i in range(1960, 2015):
    filename = 'images/lifeexp_{}.png'.format(i)
    images.append(imageio.imread(filename))

imageio.mimsave('output.gif', images, fps=3)




