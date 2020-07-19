import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import imageio


####step 1
fert = pd.read_csv('data/gapminder_total_fertility.csv', index_col=0)

#print(fert)

####step2
life = pd.read_excel('data/gapminder_lifeexpectancy.xlsx', index_col=0)


####step3

#print(life.shape)
#print(fert.shape)


####step4
#print(fert.columns)
#print(life.columns)

ncol = [int(x) for x in fert.columns]
fert.set_axis(axis=1, labels=ncol, inplace=True)
#print(fert.columns)



####step5
sfert = fert.stack()
slife = life.stack()
#print(sfert)
#print(slife)

#d = {'fertility': sfert, 'lifeexp': slife}
#df2 = pd.DataFrame(data=d)

####step6

population = pd.read_excel('data/gapminder_population.xlsx', index_col=0)

spop = population.stack()
d = {'fertility': sfert, 'lifeexp': slife, 'population':spop}
df2 = pd.DataFrame(data=d)
#print(population)


####step7

df3 = df2.stack()
df4 = df3.unstack((0,2))
#print(df2)
#print(df3)
#print(df4)

####step8
#df4[['Germany', 'France', 'Sweden']].plot()
df5 = df3.unstack(2)
#df5.plot.scatter('fertility', 'lifeexp', s=0.1)

df6 = df3.unstack(1)
df6 = df6[1950]
df6 = df6.unstack(1)
#df6.plot.scatter('fertility', 'lifeexp', s=0.1)

####step9

#cmap = plt.get_cmap('tab20', lut = len(df6)).colors
#df6.plot.scatter('fertility', 'lifeexp', s=10, c=cmap)
#plt.savefig('images/output.png')

###step10
df7 = df3.unstack(1)
for year in range(1960,2016):
    filename = 'images/lifeexp_'+str(year)+'.png'

    tmp = df7[year]
    tmp = tmp.unstack(1)
    cmap = plt.get_cmap('tab20', lut = len(tmp)).colors
    tmp.plot.scatter('fertility', 'lifeexp', s=tmp['population']/100000,c=cmap)
    plt.axis((0,10,0,100)) 
    plt.savefig(filename) 
    plt.close()

####step11

####step12

images = []

for i in range(1960, 2016):
    filename = 'images/lifeexp_{}.png'.format(i)
    images.append(imageio.imread(filename))

imageio.mimsave('output.gif', images, fps=3)



