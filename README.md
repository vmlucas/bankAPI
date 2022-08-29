# bankAPI

API service to retrieve stock data from a local DB server. 

python3.10
flask
flask_restx
pandas
json
psycopg2
sqlalchemy

#start the API server
#run python3 main.py on ./bank_API folder
#usage 
#fetch all stocks names
#http://127.0.0.1:5000/names

#fetch all stock historical data
#http://127.0.0.1:5000/stocks?stock=AAPL&init=&end=
#
#fetch stock data since a date
##http://127.0.0.1:5000/stocks?stock=AAPL&init=2022-05-20&end=
#
#fetch stock data between dates
##http://127.0.0.1:5000/stocks?stock=AAPL&init=2022-05-20&end=2022-07-01
