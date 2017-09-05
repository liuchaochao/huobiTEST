#coding=utf-8

from Util import *
import HuobiService
import requests
import json
import time

# import logging
# 
# logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='loginfo.log',
#                 filemode='w')

# 获取莱特币的K线走势，当前是001(一分线), 获取长度length=3
GET_LTC_KLINE_URL = "http://api.huobi.com/staticmarket/ltc_kline_001_json.js?length=3"

def buyMarket(current_amount):
    # 买入
    if float(current_amount) >= 0.01:
        print "买入" 
        HuobiService.buyMarket(2, current_amount ,None,None,BUY_MARKET)

def sellMarket(current_ltc):
   # 卖出
   if float(current_ltc) >= 0.01:
        print "卖出" 
        HuobiService.sellMarket(2, current_ltc,None,None,SELL_MARKET)

if __name__ == "__main__":
    #print "提交限价单接口"
    #print HuobiService.buy(1,"2355","0.01",None,None,BUY)
    #print "提交市价单接口"
    #print HuobiService.buyMarket(2,"30",None,None,BUY_MARKET)
    #print "取消订单接口"
    #print HuobiService.cancelOrder(1,68278313,CANCEL_ORDER)
    #print "获取账号详情"
    #print HuobiService.getAccountInfo(ACCOUNT_INFO)
    #print "查询个人最新10条成交订单"
    #print HuobiService.getNewDealOrders(2,NEW_DEAL_ORDERS)
    #print "根据trade_id查询order_id"
    #print HuobiService.getOrderIdByTradeId(1,274424,ORDER_ID_BY_TRADE_ID)
    #print "获取所有正在进行的委托"
    #print HuobiService.getOrders(1,GET_ORDERS)
    #print "获取订单详情"
    #print HuobiService.getOrderInfo(1,68278313,ORDER_INFO)
    #print "现价卖出"
    #print HuobiService.sell(2,"22.1","0.2",None,None,SELL)
    #print "市价卖出"
    #print HuobiService.sellMarket(2,"1.3452",None,None,SELL_MARKET)

    # 获取账号详情
    MyInfo = HuobiService.getAccountInfo(ACCOUNT_INFO)
    # 获取当前余额与莱特币数量,返回Str
    current_amount = MyInfo["available_cny_display"]
    # 获取当前莱特币数量
    current_ltc = MyInfo["available_ltc_display"]
    print MyInfo["available_cny_display"], MyInfo["available_ltc_display"]

    # 获取三分钟内的莱特币走势
    ltc_kline_json = requests.get(GET_LTC_KLINE_URL).text
    ltc_kline_json = json.loads(ltc_kline_json)

    kline_dict = {}
    key = 1
    for per_ltc_kline in ltc_kline_json:
        kline_dict[key] = per_ltc_kline[4] - per_ltc_kline[1]
        key += 1

    print kline_dict
    if kline_dict[1] <0 and kline_dict[2] <0 and kline_dict[3]>0:
        # 买入
        buyMarket(current_amount)
        print "买入"
        do = "买入"
    elif kline_dict[1] >0 and kline_dict[2] >0 and kline_dict[3]>0:
	    buyMarket(current_amount)
	    print "买入"
	    do = "买入"
    elif kline_dict[1] >0 and kline_dict[2] >0 and kline_dict[3]<0:
        # 卖出
        sellMarket(current_ltc)
        print "卖出"
        do = "卖出"
    else:
        print "不处理"
        do = "不处理"

    log_dict = {
	"time": time.strftime("%Y/%m/%d %H:%M:%S"),
        "available_cny_display": MyInfo["available_cny_display"],
        "available_ltc_display": MyInfo["available_ltc_display"],
        "kline_dict": kline_dict,
        "do": do,
    }
    f = open('log.txt', 'a')
    f.write(json.dumps(log_dict))
    f.write('\n')
    f.close()
