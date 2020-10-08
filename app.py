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
            data.append(item['stockid'])
        result['stocklist'] = data
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
