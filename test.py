from stock import PHStock
from stockdb import PHStockDB
from analysis import PHAnalysis
import requests
import pandas as pd



# Init mongodb
stockDB = PHStockDB()

result = stockDB.get_changing_stockholder_result()

print(str(result[0]))





