from typing import Any
from typing_extensions import SupportsIndex
import pandas as pd
import pyodbc as sql
from sqlalchemy import create_engine

class SQLConnector:

    def __init__(self, server='LAPTOP-P37D38OQ\SQLEXPRESS', database='TeslaTask', chunksize=10000):
        self.server = server
        self.database = database
        self.chunksize = chunksize
        self.conn_str = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
        self.conn = sql.connect(self.conn_str)
        self.cursor = self.conn.cursor()
        self.conn_str_eng = f'mssql+pyodbc://@{server}/{database}?driver=SQL+Server+Native+Client+11.0'
        self.engine = create_engine(self.conn_str_eng, fast_executemany=True)

    def execute(self, query):
        self.cursor.execute(query)

    def read(self, query):
        df_iter = pd.read_sql_query(query, self.engine, chunksize=self.chunksize)
        df = pd.concat(df_iter, ignore_index=True)
        return df
    
    def insert(self, df, tbl):
        df.to_sql(tbl, con=self.engine, index=False, if_exists='replace') 


if __name__ == "__main__":
    con = SQLConnector()
    tbls_list = ['gender_ethnicity', 'job', 'raw_data']
    for tbl in tbls_list:
        print(f'Reading {tbl}!')
        df = pd.read_csv(f"C:\\Other\\Tesla_Data_Analyst\\{tbl}.csv")
        print(f'Inserting into {tbl}!')
        con.insert(df, tbl)
        print(f'Done with {tbl}!')
    print(f'Executing UpdateTables')    
    con.execute("exec UpdateTables 'gender_ethnicity_final', 'job_final', 'combined_table'")
    print(f"Done with UpdateTables and start generating combined_table!")
    combined_df = con.read("SELECT * FROM dbo.combined_table")
    print("Start writing combined_table to csv!")
    combined_df.to_csv(r'C:\Other\Tesla_Data_Analyst\combined_df.csv')
    print("DONE!!!")
    