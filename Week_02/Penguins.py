import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

desired_width = 300

pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)

df = pd.read_csv("all_penguins_clean.csv")

df["Sex"].fillna("Missing", inplace = True)

med = df["Flipper Length (mm)"].median()

df["Flipper Length (mm)"].fillna(med, inplace = True)

# missing = df.isnull()
#
# sns.heatmap(missing)
#
# plt.show()


OH = pd.get_dummies(df["Sex"])

df2 = pd.concat([df, OH])
df2 = df2.drop(columns = ["Sex","."])
print(df2)