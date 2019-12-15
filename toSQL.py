# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:39:06 2019

@author: juliochristian
"""


import pandas as pd
from sqlalchemy import create_engine
import urllib
from os import listdir,path
import pyodbc

params = urllib.parse.quote_plus('Driver={SQL Server Native Client 11.0};'
                      'Server=JULIO\SQLEXPRESS;'
                      'Database=AdvDB Project;'
                      'Trusted_Connection=yes;')


sourcePath = 'G:\Documentos\MasterDegree\BDMA\Classes\Advanced DB\Project\data\DataNormalized'


for file in listdir(sourcePath):
    if file.endswith(".csv"):
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        tableName = path.splitext(file)[0]
        print('Table Name: ' + tableName + '\n')
        csv_table = pd.read_csv(sourcePath + "/"+file, encoding = "ISO-8859-1")
        csv_table.to_sql(tableName, engine,if_exists='append', chunksize=10, index = False)
        engine.dispose()
        
        
        