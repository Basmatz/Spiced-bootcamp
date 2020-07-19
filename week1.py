# -*- coding: utf-8 -*-
''''
WEEK 1  EXERCISE Alex Metz
'''
"""
Created on Wed Jul 15 16:54:33 2020

@author: Besitzer
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#
fert = pd.read_csv('gapminder_total_fertility.csv', index_col=0)
#change format of fert header to int, inplace=True : creates new instance
#fert.set_axis(labels=[int(i) for i in fert.columns], axis='columns', inplace=True)
# better way
fert.set_axis(labels=fert.columns.astype(int), axis='columns', inplace=True)
life= pd.read_excel('gapminder_lifeexpectancy.xlsx',index_col=0)
pop = pd.read_excel('gapminder_population.xlsx.',index_col=0)
#
d = {'fertility': fert.stack(), 'lifeexp': life.stack(), 'population': pop.stack()}
#print(d)
#
df2 = pd.DataFrame(data=d)
#print(df2.head(5))
df3 = df2.stack()
#print(df3.head(5))
#print('------------------------')
df4= df3.unstack((0,2))
#print(df4.head(5))
#df4[['Germany', 'France', 'Sweden']].plot()
#
df5 = df3.unstack(2)
#df5.plot.scatter('fertility', 'lifeexp', s=0.1)
#print('------------------------')
#print(df3.head(5))
#print('------------------------')
#print(df5.head(5))
#print('------------------------')
#
df6 = df3.unstack(1)
df6 = df6.unstack(1)
#print(df6.head(5))
#
#
country=['China','India','Indonesia','Pakistan']
#
plt.figure(10,figsize=(12,7))
df8=df6[2015]
for pop in np.linspace(df8['population'].max()/5,df8['population'].max(),5):
    plt.scatter([], [], c='k', alpha=0.3, s=pop/1e6, label='%.2g'%pop) 
    plt.legend()
#
ax = plt.axes()
ax.set_xlabel('Fertility')
ax.set_ylabel('Life expectancy')
cmap = plt.get_cmap('tab20', lut = len(df6[1950])).colors
#
#iterate in years series
#
for i in fert.columns[-100:]:        
    plt.title('Relation fertility, Life expectancy and population %i'%i , size=18)
    df61=df6[i]
    sc= ax.scatter(df61['fertility'], df61['lifeexp'], s=df61['population']/1e6, c=cmap, alpha=.5)
    ann= list()
    for c in country:
        ann.append(ax.annotate(c, xy=( df61.loc[c,'fertility'], df61.loc[c,'lifeexp'] ) ) )
    plt.draw()
    plt.pause(.05) if i < 1950 else plt.pause(.5) 
    if i != fert.columns[-1]:       
        sc.remove()     
        for a in ann:
            a.remove()
        