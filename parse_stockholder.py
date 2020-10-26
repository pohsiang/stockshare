from stock import PHStock
from stockdb import PHStockDB
from pymongo import MongoClient
import requests
import pandas as pd

def record_single_stock(stock_index):
    stock = PHStock(stock_index)
    stockholder_detail = stock.get_stockholder_detail()
    if stockholder_detail is None:
        return
    stockDB.add_single_stock_stockholder(stockholder_detail)
    print("ID:" + str(stock_index))

def get_all_stockid():
    # Init stock_index_list from TW Stock Index
    link = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL"
    r = requests.get(link)
    stockid_list = []
    stock_data = pd.DataFrame(r.json()['data'])
    stock_data.columns = ['STOCK_INDEX', 'NAME', 'VOLUME', 'AMOUNT', 'OPEN',
                'HIGH', 'LOW', 'CLOSE', 'PRICE_CHANGE', 'TRANSACTION']
    total_rows_stock_data = len(stock_data.index)
    for row_idx in range(total_rows_stock_data):
        stockid_list.append(stock_data['STOCK_INDEX'].iloc[row_idx])
    return stockid_list


# Init mongodb
stockDB = PHStockDB()
stockid_list = get_all_stockid()
total_stockid = len(stockid_list)
stockDB.clear_stockhodler()

index = 0
for stockid in stockid_list:
    record_single_stock(stockid)
    print("Progress:" + str(index) + "/" + str(total_stockid))
    index = index + 1










