# -*- coding: utf-8 -*
import requests
from lxml import html
import sys
import chardet

class PHStock:

    def __init__(self, stock_id):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.stock_id = stock_id

    def get_dividend(self):
        url = 'https://tw.stock.yahoo.com/d/s/dividend_'+str(self.stock_id)+'.html'
        page = requests.get(url, headers=self.headers)
        tree = html.fromstring(page.content)
        value = tree.xpath("//tr[@bgcolor='#FFFFFF']/td[6]/text()")
        return value

    def get_price(self):
        url = 'https://tw.stock.yahoo.com/q/q?s='+str(self.stock_id)
        page = requests.get(url, headers=self.headers)
        tree = html.fromstring(page.content)
        value = tree.xpath("//td[@bgcolor='#FFFfff'][2]/b/text()")
        return value[0]

    def get_who_buy(self):
        url = 'https://tw.stock.yahoo.com/d/s/major_'+str(self.stock_id)+'.html'
        page = requests.get(url, headers=self.headers)
        print (requests.utils.get_encodings_from_content(page.content))
        page.encoding = "big5"
        tree = html.fromstring(page.text)
        #print page.text
        result = {}
        who_buy = tree.xpath("//td[@class='ttt'][1]/text()") # Need +1
        who_buy.pop(0)
        who_buy.pop(0)
        who_buy_total_volume = tree.xpath("//td[@class='ttt'][4]/text()")
        who_buy_total_volume.pop(0)
        who_sell = tree.xpath("//td[@class='ttt'][5]/text()")
        who_sell.pop(0)
        who_sell_total_volume = tree.xpath("//td[@class='ttt'][8]/text()")
        who_sell_total_volume.pop(0)
        for idx, who in enumerate(who_buy):
            if who is None:
                break;
            print ("who:" + who)
            print ("who_buy_volume:" + who_buy_total_volume[idx])
        print ("========")
        for idx, who in enumerate(who_sell):
            if who is None:
                break;
            print ("who:" + who)
            print ("who_sell_volume:" + who_sell_total_volume[idx])

    # Parse StockHolder website
    def get_stockholder_detail(self):
        url = 'https://norway.twsthr.info/StockHolders.aspx?stock=' + str(self.stock_id)
        page = requests.get(url, headers=self.headers)
        tree = html.fromstring(page.content)
        data = {}
        #ID
        data['stock_id'] = self.stock_id
        #名稱
        name = tree.xpath("//div[@class='navbar-inner']//li[@class='dropdown']//ul[@class='dropdown-menu']//a/text()")
        if not name:
            return None
        data['stock_name'] = name[0].split(" ")[1]
        #資料日期
        date_list = tree.xpath("//div[@id='D1']//table//td[3]/text()")
        if not date_list:
            return None
        date_list.pop(0)
        date_list = self.remove_space_in_datalist(date_list)
        data['date_list'] = date_list
        #總股東人數
        allstockholder_list = tree.xpath("//div[@id='D1']//table//td[5]/text()")
        allstockholder_list.pop(0)
        allstockholder_list.pop(0)
        data['allstockholder'] = allstockholder_list
        #平均張數
        averagestockperperson_list = tree.xpath("//div[@id='D1']//table//td[6]/text()")
        averagestockperperson_list.pop(0)
        data['averagestockperperson'] = averagestockperperson_list
        #大於 400 張的股東持有張數
        allstock_over400stockholder_list = tree.xpath("//div[@id='D1']//table//td[7]/text()")
        allstock_over400stockholder_list.pop(0)
        allstock_over400stockholder_list.pop(0)
        data['allstock_over400stockholder'] = allstock_over400stockholder_list
        #大於 400 張的股東持有百分比
        percentage_over400stockholder_list = tree.xpath("//div[@id='D1']//table//td[8]/text()")
        percentage_over400stockholder_list.pop(0)
        percentage_over400stockholder_list.pop(0)
        data['percentage_over400stockholder'] = percentage_over400stockholder_list
        #大於 400 張的股東人數
        people_over400stockholder_list = tree.xpath("//div[@id='D1']//table//td[9]/text()")
        people_over400stockholder_list.pop(0)
        people_over400stockholder_list.pop(0)
        data['people_over400stockholder'] = people_over400stockholder_list
        #大於 400 張小於 600 張股東人數
        people_over400less600stockholder_list = tree.xpath("//div[@id='D1']//table//td[10]/text()")
        people_over400less600stockholder_list.pop(0)
        data['people_over400less600stockholder'] = people_over400less600stockholder_list
        #大於 600 張小於 800 張股東人數
        people_over600less800stockholder_list = tree.xpath("//div[@id='D1']//table//td[11]/text()")
        people_over600less800stockholder_list.pop(0)
        data['people_over600less800stockholder'] = people_over600less800stockholder_list
        #大於 800 張小於 1000 張股東人數
        people_over800less1000stockholder_list = tree.xpath("//div[@id='D1']//table//td[12]/text()")
        people_over800less1000stockholder_list.pop(0)
        data['people_over800less1000stockholder'] = people_over800less1000stockholder_list
        #大於 1000 張股東人數
        people_over1000stockholder_list = tree.xpath("//div[@id='D1']//table//td[13]/text()")
        people_over1000stockholder_list.pop(0)
        data['people_over1000stockholder'] = people_over1000stockholder_list
        #大於 1000 張的股東持有百分比
        percentage_over1000stockholder_list = tree.xpath("//div[@id='D1']//table//td[14]/text()")
        percentage_over1000stockholder_list.pop(0)
        percentage_over1000stockholder_list.pop(0)
        data['percentage_over1000stockholder'] = percentage_over1000stockholder_list

        if len(allstockholder_list) == len(averagestockperperson_list) == len(allstock_over400stockholder_list) == len(percentage_over400stockholder_list) == len(people_over400stockholder_list) == len(people_over400less600stockholder_list) == len(people_over600less800stockholder_list) == len(people_over800less1000stockholder_list) == len(people_over1000stockholder_list) == len(percentage_over1000stockholder_list):
            print("Correct")
        else:
            print("Incorrect")
            return None

        return data

    def remove_space_in_datalist(self, data_list):
        for idx in range(len(data_list)):
            data_list[idx] = data_list[idx].replace(u'\xa0', u'')
        return data_list

    def print_datalist(self, data_list):
        for data in data_list:
            print(data)
