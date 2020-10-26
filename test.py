from stock import PHStock
from stockdb import PHStockDB
from analysis import PHAnalysis
import requests
import pandas as pd

from lxml import html
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# Init mongodb
stockDB = PHStockDB()

url = 'https://norway.twsthr.info/StockHolders.aspx?stock=1234'
page = requests.get(url, headers=headers)
tree = html.fromstring(page.content)

name = tree.xpath("//div[@class='navbar-inner']//li[@class='dropdown']//ul[@class='dropdown-menu']//a/text()")
print(name[0].split(" ")[1])





