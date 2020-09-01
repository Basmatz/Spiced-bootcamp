import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd
import inspect


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

df_employees = pd.DataFrame(pd.read_csv('/home/stazhe/Spiced/logistic-lemongrass-student-code/week_06/data/employees.csv'))
df_employees.drop(columns=['photo','notes','photoPath'], inplace=True)
column_names = [*df_employees]
print(column_names)

class Employee(Base):
    
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    lastname = Column(String)
    firstname = Column(String)
    title = Column(String)
    courtesy = Column(String)
    birthdate = Column(DateTime)
    hiredate = Column(DateTime)
    address = Column(String)
    city = Column(String)
    region = Column(String)
    postcode = Column(String)
    country = Column(String)
    phone = Column(String)
    extension = Column(String)
    reports_to = Column(Integer, ForeignKey('employees.id'))
    
    def __repr__(self):
        return f'User {self.name}'

employee_attr = dir(Employee)
for attr in employee_attr:
    if '__' in str(attr):
        employee_attr.pop(attr)
print(employee_attr)

for index, row in df_employees.iterrows():
    employee = Employee(id= row['employeeID'], 
                        lastname = Column(String),
                        firstname = Column(String)
                        title = Column(String)
                        courtesy = Column(String)
                        birthdate = Column(DateTime)
                        hiredate = Column(DateTime)
                        address = Column(String)
                        city = Column(String)
                        region = Column(String)
                        postcode = Column(String)
                        country = Column(String)
                        phone = Column(String)
                        extension = Column(String)
                        reports_to = Column(Inte )
    session.add(shipper)
    print (shipper.id)