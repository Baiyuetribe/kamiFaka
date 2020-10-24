# *-* coding: UTF-8 *-*

import hashlib,time,json
import requests
# import qrcode
from urllib.parse import urlencode, unquote_plus


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]



class Hupi(object):
    # def __init__(self):
    #     self.appid = "201906121518"  #在虎皮椒V3申请的appid
    #     self.AppSecret = "5473e7cf20185a8f90b87eb2de717845"  #在虎皮椒V3申请的AppSecret
    #     self.notify_url = 'http://7053a6c10b98.ngrok.io/notify'     #公网访问接口
    #     self.return_url = 'http://7053a6c10b98.ngrok.io/return' #支付成功后的跳转地址
    #     self.callback_url = 'http://7053a6c10b98.ngrok.io'  #取消支付后的跳转地址
    def __init__(self,payment='wechat'):         #！！！通知、回调、callback都不能留空
        from service.util.pay.pay_config import get_config
        notify_url='http://7053a6c10b98.ngrok.io/notify'
        return_url='http://7053a6c10b98.ngrok.io/return'
        callback_url='http://7053a6c10b98.ngrok.io'
        if payment == 'wechat':
            config = get_config('虎皮椒微信')

        else:
            config = get_config('虎皮椒支付宝')
        self.appid = config['appid'] #数据库返回微信的APPID和SECRET
        self.AppSecret = config['AppSecret'] #数据库返回微信的APPID和SECRET
        self.payment = payment            
        self.notify_url = notify_url
        self.return_url = return_url
        self.callback_url = callback_url
    def curl(self, data, url):
        data['hash'] = self.sign(data)
        #print(data)
        headers = {"Referer":"http://7053a6c10b98.ngrok.io/"}  #自己的网站地址
        r = requests.post(url, data=data,headers=headers)
        return r

    def sign(self, attributes):
        attributes = ksort(attributes)
        #print(attributes)
        m = hashlib.md5()
        #print(unquote_plus(urlencode(attributes)))
        m.update((unquote_plus(urlencode(attributes))  + self.AppSecret).encode(encoding='utf-8'))
        sign = m.hexdigest()
        #sign = sign.upper()
        #print(sign)
        return sign

    def Pay(self,trade_order_id,total_fee,title):   #订单编号，支付方式，价格，标题
        url = "https://api.xunhupay.com/payment/do.html"
        data = {
            "version":"1.1",
            "lang":"zh-cn",
            "plugins":"flask",
            "appid":self.appid,
            "trade_order_id":trade_order_id,
            "payment":self.payment,
            "is_app":"Y",
            "total_fee":total_fee,
            "title":title,
            "description":"",
            "time":str(int(time.time())),
            "notify_url":self.notify_url, #回调URL（订单支付成功后，WP开放平台会把支付成功消息异步回调到这个地址上）
            "return_url":self.return_url, #支付成功url(订单支付成功后，浏览器会跳转到这个地址上)
            "callback_url":self.callback_url,#商品详情URL或支付页面的URL（移动端，商品支付失败时，会跳转到这个地址上）
            "nonce_str":str(int(time.time())), #随机字符串(一定要每次都不一样，保证请求安全)
        }
        return self.curl(data, url)

    def Check(self,out_trade_order):   #回调检测
        url = "https://api.xunhupay.com/payment/query.html"
        data = {
            "appid":self.appid,
            "out_trade_order":out_trade_order,
            "time":str(int(time.time())),
            "nonce_str":str(int(time.time())), #随机字符串(一定要每次都不一样，保证请求安全)
        }
        return self.curl(data, url)

def payment():
    pass

if __name__ == "__main__":
    obj = Hupi()
    order_id = '45455154444441212'
    r = obj.Pay(order_id,"0.1","test")
    print(r,r.text)
    print(r.json()["url"])
    print('='*15)
    c = obj.Check(out_trade_order=order_id)
    print(c.text)