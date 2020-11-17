from stock import PHStock
from stockdb import PHStockDB
from analysis import PHAnalysis
import requests

def get_one_month_data(data_list):
    result = []
    copy_data_list = data_list.copy()
    for i in range(1, 5):
        result.append(copy_data_list.pop(0))
    return result

def get_one_year_data(data_list):
    result = []
    copy_data_list = data_list.copy()
    data_list_length = len(copy_data_list)
    length = 51
    if 51 > data_list_length:
        length = data_list_length
    for i in range(1, length):
        result.append(copy_data_list.pop(0))
    return result

# Init mongodb
stockDB = PHStockDB()
stock_analysis = PHAnalysis()

stockid_list = stockDB.get_all_stockid()
stockDB.clear_changing_stockholder_result()
for stockid in stockid_list:
    raw = stockDB.get_single_stock_stockholder(stockid)
    stock = raw[0]

    # Check
    if not stock['percentage_over1000stockholder'] or not stock['percentage_over400stockholder']:
        print(stockid +":Empty")
        continue
    if len(stock['percentage_over1000stockholder']) < 10:
        print(stockid +":Not Enough data")
        continue
    # All over 1000 sd
    stock_percentage_over1000stockholder = stock['percentage_over1000stockholder']
    result_1000 = stock_analysis.get_list_sd(get_one_year_data(stock_percentage_over1000stockholder))
    # One month over 1000 sd
    stock_percentage_over1000stockholder_one_month = get_one_month_data(stock_percentage_over1000stockholder)
    result_1000_one_month = stock_analysis.get_list_sd(stock_percentage_over1000stockholder_one_month)

    # All over 400 sd
    stock_percentage_over400stockholder = stock['percentage_over400stockholder']
    result_400 = stock_analysis.get_list_sd(get_one_year_data(stock_percentage_over400stockholder))
    # One month over 400 sd
    stock_percentage_over400stockholder_one_month = get_one_month_data(stock_percentage_over400stockholder)
    result_400_one_month = stock_analysis.get_list_sd(stock_percentage_over400stockholder_one_month)

    # Record who change alot in this month
    changing_stockholder_data = {}
    changing_stockholder_data['stockid'] = stockid
    changing_stockholder_data['stock_name'] = stock['stock_name']
    if result_400_one_month > result_400 and result_1000_one_month > result_1000:
        print(str(stockid) + "," + stock['stock_name'] + ", result_400_one_month:" + str(result_400_one_month) + ", result_400:" + str(result_400) + ", result_1000_one_month:" + str(result_1000_one_month) + ", result_1000:" + str(result_1000) )
        stockDB.add_changing_stockholder_result(changing_stockholder_data)










