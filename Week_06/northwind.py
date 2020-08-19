###### Imports

#%%
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

##### Setting up connection with server

conns = 'postgres://postgres:postgres@localhost:5433/northwind'

db = create_engine(conns, encoding='latin1', echo=False)

query = "SELECT * FROM orders;"

df = pd.read_sql(query, db)
print(df)