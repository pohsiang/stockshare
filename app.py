# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api
from stockdb import PHStockDB

app = Flask(__name__)
api = Api(app)

class ChangingStackHolder(Resource):

    def __init__(self):
        self.db = PHStockDB()

    def get(self):
        cursor = self.db.get_changing_stockholder_result()
        result = {}
        data = []
        for item in cursor:
            stock = {}
            stock['stock_id'] = item['stockid']
            stock['stock_name'] = item['stock_name']
            data.append(stock)
        result['stocklist'] = data
        print(result)
        return result

class StackHodlerDetail(Resource):

    def __init__(self):
        self.db = PHStockDB()

    def get(self, stockid):
        cursor = self.db.get_single_stock_stockholder(stockid)
        result = {}
        for item in cursor:
            result = item

        result.pop('_id')
        print(result)
        return result

api.add_resource(ChangingStackHolder, '/changing')
api.add_resource(StackHodlerDetail, '/stock/<string:stockid>')


if __name__ == '__main__':
    app.run()
