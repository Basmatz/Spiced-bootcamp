#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 12:28:07 2020

@author: stazhe
"""
import pandas as pd
weather_data = pd.read_csv('~/Desktop/Spiced/logistic-lemongrass-student-code/week_05/ECA_blended_custom/weather_data.txt', sep =',' , skiprows = 19)

df = pd.DataFrame(weather_data)
df.columns=df.columns.map(str.strip)
df.drop("SOUID", axis=1, inplace=True)

df["DATE"] = pd.to_datetime(df["DATE"], format='%Y%m%d')
df.set_index("DATE", inplace=True)
print(df.head())

print(df["Q_TG"].value_counts())

print(df.loc[df['Q_TG']==9].groupby("Month"))
