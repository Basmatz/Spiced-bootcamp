import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pandas as pd


#from sqlalchemy import create_engine

# HOST = 'logisticlemongrass.c1ipxvq2s9x8.eu-central-1.rds.amazonaws.com'
# PORT = '5432'
# USER = 'postgres'
# PASSWORD = 'titanic99'
# DATABASE = 'anastasia'

# conn_string = f'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
# engine = s.create_engine(conn_string)

# db = s.create_engine("sqlite:///northwind.db")
# db.table_names()
# drop = "DROP TABLE customers"
# db.execute(drop)
# customers = pd.read_csv('/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/customers.csv')

# customers.to_sql('customers', db)
# db.table_names()

# query = "SELECT * FROM customers;"

# df = pd.read_sql(query, db)
# print(df.head())

engine = s.create_engine("sqlite:///northwind.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

####


class Shipper(Base):
    __tablename__ = 'shippers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f'User {self.name}'

df_ship = pd.DataFrame(pd.read_csv('/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/shippers.csv'))

for index, row in df_ship.iterrows():
    shipper = Shipper(id= row['shipperID'], name=row['companyName'], phone=row['phone'])
    session.add(shipper)
    print (shipper.id)
