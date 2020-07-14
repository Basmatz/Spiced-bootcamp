import pandas as pd
# 1. read the file into a DataFrame
df = pd.read_csv("continents.csv", sep=';')

# 2. display the number of rows and columns
#print(df.info())


# 3. display the first 5 countries in the alphabet
#print(df.country.head())

print(df.head())
print()
# 4. which continent has the most countries?
print(df.groupby("continent").count().idxmax())
print()
print(df.groupby("continent").count().nlargest(1, "country"))
print("\n\n\n")


# 5. find out on which continent Cyprus is
print(df.loc[(df["country"] == "Cyprus")].continent.item())
print("\n\n\n")
# 6. define a DataFrame with all African countries
africa = df.loc[(df["continent"] == "Africa")].country.to_string(index = False)
print(africa)
print("\n\n\n")
# 7. define a DataFrame with countries 80 through 100
subset = df.country.iloc[80:101]
print(subset)
print("\n\n\n")
# 8. select every second country
print(df.country.iloc[::2])
print("\n\n\n")

# 9. select 10 random countries
import random
print(df.country.iloc[random.sample(range(len(df)), 10)])
print("\n\n\n")

# 10. select all countries having two or more a`s
print(df["country"].loc[(df['country'].str.count("a")>1)])