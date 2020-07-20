import plotly.express as px
import pandas as pd

#Import Data:
df = pd.read_csv("gapminder_total_fertility.csv")
df2 = pd.read_excel("gapminder_lifeexpectancy.xlsx")
df3 = pd.read_excel("gapminder_population.xlsx")

#Transform Columns
df = df.melt(id_vars="Total fertility rate",
        var_name="year",
        value_name="fertility")

df.rename(columns={"Total fertility rate": "country"}, inplace=True)

df2 = df2.melt(id_vars="Life expectancy",
        var_name="year",
        value_name="life expectancy")

df2.rename(columns={"Life expectancy": "country"}, inplace=True)


df3 = df3.melt(id_vars="Total population",
        var_name="year",
        value_name="population")

df3.rename(columns={"Total population": "country"}, inplace=True)

#Change String values to Int
df["year"] = df["year"].astype(int)


df4 = pd.merge(df,df2, how='inner', on=["country","year"])
df4 = pd.merge(df4,df3, how='inner', on=["country","year"])

print(df4)

df4.dropna(inplace=True)


print(df3.where(df3["year"]>1960))

fig = px.scatter(df4.loc[(df4["year"] >= 1960)],
                 x="life expectancy",
                 y="fertility",
                 animation_frame="year",
                 animation_group="country",
                 size="population",
                 color="country",
                 size_max=60,
                 hover_name="country",
                 range_x=[20,90],
                 range_y=[0,10])

fig.layout.update(showlegend=False)

fig.show()