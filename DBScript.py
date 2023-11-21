import pandas as pd
import pyodbc as sql
from sqlalchemy import create_engine

class SQLConnector:

    def __init__(self, server='LAPTOP-P37D38OQ\SQLEXPRESS', database='TeslaTask', chunksize=1000):
        self.server = server
        self.database = database
        self.chunksize = chunksize
        self.conn_str = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
        # self.conn = sql.connect(self.conn_str)
        # self.cursor = self.conn.cursor()
        self.conn_str_eng = f'mssql+pyodbc://@{server}/{database}?driver=SQL+Server+Native+Client+11.0'
        self.engine = create_engine(self.conn_str_eng)



    def read(self, query):
        df_iter = pd.read_sql(query, self.engine, chunksize=self.chunksize)
        df = pd.concat(df_iter, ignore_index=True)
        return df
    
    def insert(self, df):
        df.to_sql('job', con=self.engine, index=False, if_exists='replace') 


con = SQLConnector()

df = pd.read_csv(r'C:\Other\Tesla_Data_Analyst\job.csv')

con.insert(df)

 