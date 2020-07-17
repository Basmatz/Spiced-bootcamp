import pandas as pd
import matplotlib.pyplot as plt

lifeexp = pd.read_excel("gapminder_lifeexpectancy.xlsx")

#lifeexp = lifeexp[[1950, 1975, 2000, 2015]]


lifeexp.set_index("Life expectancy", inplace=True)

print(lifeexp)

#plt.savefig('histo.png')

colname = 2015

#lifeexp[colname].hist(bins=5)
#lifeexp[colname].hist(bins=10)
lifeexp[colname].hist(color='green', alpha=0.75, histtype='bar',bins=5)

plt.title('Global Life Expectancy')
plt.xlabel('Age')
plt.ylabel('Frequency')

plt.axis([0.0, 90.0, 0.0, 85.0])

plt.savefig('histo.svg')
plt.show()