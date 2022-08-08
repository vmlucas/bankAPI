from flask import Flask,request
from flask_restx import Api, Resource, reqparse
from src.model.dataModel import fetchStocks
from src.server.instance import server

app, api = server.app, server.api

@api.route('/stocks')
class StockList(Resource):
    def get(self,):
        args = request.args
        return fetchStocks(args['stock'],args['init'],args['end'])