from http import server
from src.server.instance import server
from src.controllers.stocks import *

server.run()

#usage http://127.0.0.1:5000/stocks?stock=AAPL&init=2022-05-20&end=