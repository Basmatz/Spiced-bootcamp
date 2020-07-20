import pandas as pd
import matplotlib.pyplot as plt
import imageio

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 25)
pd.set_option('display.width', 1000)

df = pd.read_csv('gapminder_total_fertility.csv', index_col=0)
df2 = pd.read_excel('gapminder_lifeexpectancy.xlsx', index_col=0)
pop = pd.read_excel('gapminder_population.xlsx', index_col=0)

df.columns = df.columns.astype("int")

print(df)

df = df.stack()

df2 = df2.stack()
pop = pop.stack()


df3 = pd.concat([df, df2, pop], axis=1)
df3.rename(columns={0: "fertility",1: "lifeexp", 2: "population"}, inplace=True)
df3.index.names = ["country", "year"]
print(df3)

df3 = df3.stack()

df4 = df3.unstack((0,2))

df5 = df3.unstack((2))

df5.plot.scatter('fertility', 'lifeexp', s=0.1)

df6 = df3.unstack(1)


df6 = df6.unstack(1)
print(df6)

#cmap = plt.get_cmap('tab20', lut = len(df6)).colors


# for i in list(range(1960,2016)):
#     df6[i].plot.scatter('lifeexp', 'fertility',
#                         s=df6[i]['population']*0.000001,
#                         c=cmap,
#                         xlim=[20,90],
#                         ylim=[0,10],
#                         title="Year: " + str(i),
#                         figsize = (16,9))
#     plt.savefig(str(i) + '.png', dpi=200)
#
# images = []
#
# for i in list(range(1960,2016)):
#
#     filename = '{}.png'.format(i)
#     images.append(imageio.imread(filename))
#
# imageio.mimsave('output.gif', images, fps=8)