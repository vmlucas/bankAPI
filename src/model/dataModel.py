import pandas as pd
from pandas import DataFrame 
import json
import psycopg2
import sqlalchemy as db
from sqlalchemy import create_engine,text
import numpy
from psycopg2.extensions import register_adapter, AsIs


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

#connect to the PostgreSQL on localhost
def getEngine():
    engine = db.create_engine('postgresql+psycopg2://postgres:vsvLL430@localhost/postgres')
    return engine   



def fetchStocks(valor,init,end):    
    engine = getEngine()
    if( len(init) ):
       if( len(end) ):
         s = text("select *  from bank.stocks where stockname = :n and TO_DATE(date_value ,'YYYY-MM-DD') >= TO_DATE(:i,'YYYY-MM-DD') and TO_DATE(date_value ,'YYYY-MM-DD') < TO_DATE(:e,'YYYY-MM-DD' )")
         result = engine.execute(s, n=valor,i=init,e=end)
         return json.dumps([ row._asdict() for row in result ])
       else: 
         s = text("select *  from bank.stocks where stockname = :n and TO_DATE(date_value ,'YYYY-MM-DD') >= TO_DATE(:i,'YYYY-MM-DD')")
         result = engine.execute(s, n=valor,i=init)
         return json.dumps([ row._asdict() for row in result ])
    else:   
       s = text('select *  from bank.stocks where stockname = :n') 
       result = engine.execute(s, n=valor)
       return json.dumps([ row._asdict() for row in result ])
    
''''
stockname text NULL,
	date_value text NULL,
	open_value float8 NULL,
	high_value float8 NULL,
	low_value float8 NULL,
	close_value float8 NULL,
	adj_close_value float8 NULL,
	volume
'''    

