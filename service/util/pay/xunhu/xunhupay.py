# *-* coding: UTF-8 *-*

import hashlib,time,json
import requests
# import qrcode
from urllib.parse import urlencode, unquote_plus


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]

class Xunhu(object):
    def __init__(self,payment='wechat'):         #！！！通知、回调、callback都不能留空
        from service.util.pay.pay_config import get_config
        self.web_url = get_config('web_url')
        if payment == 'wechat':
            config = get_config('迅虎微信')
        else:
            config = get_config('迅虎支付宝')
        self.appid = config['ID'] #数据库返回微信的APPID和SECRET
        self.AppSecret = config['Key'] #数据库返回微信的APPID和SECRET
        self.API = 'https://admin.xunhuweb.com' # 支持两种API模式：api.xunhupay.com和、api.vrmrgame.com，admin.xunhupay.com不支持
        self.payment = payment            
        self.notify_url = self.web_url + '/notify/xunhupay0'
    def curl(self, data, url):
        data['hash'] = self.sign(data)
        #print(data)
        headers = {"Referer":self.web_url}  #自己的网站地址
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
        url = self.API+'/pay/payment'
        data = {
            "mchid":self.appid,
            "out_trade_no":trade_order_id,
            "total_fee":total_fee,
            "body":title,
            "notify_url":self.notify_url, #回调URL（订单支付成功后，WP开放平台会把支付成功消息异步回调到这个地址上）
            "type":self.payment,#
            "nonce_str":str(int(time.time())), #随机字符串(一定要每次都不一样，保证请求安全)
            "title":title,
        }
        pay_order = self.curl(data, url)
        try:
            print(pay_order.json())
            if pay_order.json()['return_code'] == 'success':
                return {'qr_code':pay_order.json()['code_url']}
        except:
            pass
        return False

    def Check(self,out_trade_order):   #回调检测
        url = self.API+'/pay/query'
        data = {
            "appid":self.appid,
            "out_trade_order":out_trade_order,
            "time":str(int(time.time())),
            "nonce_str":str(int(time.time())), #随机字符串(一定要每次都不一样，保证请求安全)
        }
        result = self.curl(data, url)
        if result.json()['data']['status'] == "OD":  #OD(支付成功)，WP(待支付),CD(已取消)
            return True
        return False

    def verify(self,data):     #异步通知    这里data=request.from
        try:
            signature = data['hash']
            data.pop('hash')
            return signature == self.sign(data)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False    
