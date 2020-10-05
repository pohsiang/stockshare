from pymongo import MongoClient

class PHStockDB:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client["stock"]

    def get_all_stockid(self):
        col = self.db["stockholder"]
        result = []
        all_stock = col.find()
        for stock in all_stock:
            result.append(stock["stock_id"])
        return result

    def clear_stockhodler(self):
        col = self.db["stockholder"]
        col.delete_many({})

    def add_single_stock_stockholder(self, data):
        col = self.db["stockholder"]
        col.insert_one(data)

    def get_single_stock_stockholder(self, stockid):
        col = self.db["stockholder"]
        query = {"stock_id": stockid}
        return col.find(query)

    def clear_changing_stockholder_result(self):
        col = self.db["changing_stockholder"]
        col.delete_many({})

    def add_changing_stockholder_result(self, data):
        col = self.db["changing_stockholder"]
        col.insert_one(data)

    def get_changing_stockholder_result(self):
        col = self.db["changing_stockholder"]
        return col.find()

       



