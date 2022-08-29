from flask import Flask,request
from flask_restx import Api, Resource, reqparse
from src.model.dataModel import fetchStocks
from src.server.instance import server
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import os
from dotenv import load_dotenv

load_dotenv("./vars/.env")

db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_name = os.getenv('db_name')

app, api = server.app, server.api
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'postgresql+psycopg2://'+db_user+':'+db_pass+'@localhost/'+db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Stock(db.Model):
    __table_args__ = {"schema": "bank"} 
    __tablename__ = 'stocks'
    id =  db.Column(db.INT,primary_key = True)
    stockname = db.Column(db.VARCHAR)
    date_value = db.Column(db.DATETIME)
    open_value = db.Column(db.Float)
    high_value = db.Column(db.Float)
    low_value = db.Column(db.Float)
    close_value = db.Column(db.Float)
    adj_close_value = db.Column(db.Float)
    volume = db.Column(db.Float)
	       
    def get_id(self):
        return str(self.id)

        
def format_stock(Stock):
    return {
        "Name": Stock.stockname,
        "data": Stock.date_value,
        "Open": Stock.open_value, 
        "High": Stock.high_value, 
        "Low": Stock.low_value, 
        "Close": Stock.close_value, 
        "Adj_close": Stock.adj_close_value, 
        "Volume": Stock.volume 
    }

#get the stocks data
@app.route('/stocks',methods=['GET'])
def getStocks():
        args = request.args
        name = args['stock']
        init = args['init']
        end = args['end']
        if( len(init) ):
          if( len(end) ):
             stocks = Stock.query.filter(Stock.stockname == name).filter(Stock.date_value >= init).filter(Stock.date_value < end).order_by(Stock.date_value.asc())
          else:    
             stocks = Stock.query.filter(Stock.stockname == name).filter(Stock.date_value >= init).order_by(Stock.date_value.asc())
        else:  
          stocks = Stock.query.filter(Stock.stockname == name).order_by(Stock.date_value.asc())

        stocks_list = []
        for stock in stocks:
            stocks_list.append(format_stock(stock))
        return {"stocks":stocks_list}



@app.route('/names',methods=['GET'])
def getNames():
        names_list = []
        for stock in Stock.query.distinct(Stock.stockname).order_by(Stock.stockname.asc()):
            names_list.append(stock.stockname)

        return {"names":names_list}


#http://127.0.0.1:5000/insert
@app.route('/insert',methods=['POST'])
def insertStocks():
        stocks = request.get_json()
        stocks_entries = []
        for s in stocks["stocks"]:
            new_entry = Stock( stockname = s['stockname'],
                           date_value = s['date_value'],
                           open_value = s['open_value'],
                           high_value = s['high_value'],
                           low_value = s['low_value'],
                           close_value = s['close_value'],
                           adj_close_value = s['adj_close_value'],
                           volume = s['volume'] )
            stocks_entries.append(new_entry)
   
        db.session.add_all(stocks_entries)
        db.session.commit()
   
        #remove duplicates
        # Create a query that identifies the row for each domain with the lowest id
        inner_q = db.session.query(sa.func.min(Stock.id)).group_by(Stock.stockname, Stock.date_value)
        aliased = sa.alias(inner_q)
        # Select the rows that do not match the subquery
        q = db.session.query(Stock).filter(~Stock.id.in_(aliased))

        # Delete the unmatched rows (SQLAlchemy generates a single DELETE statement from this loop)
        for s in q:
          db.session.delete(s)
        db.session.commit()
     
        return "stocks Loaded"