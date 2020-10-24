from os import name
from time import sleep
import requests
import time
import hashlib
from urllib.parse import urlencode,unquote


class Payjs:

    def __init__(self):
        from service.util.pay.pay_config import get_config
        config = get_config('PAYJS微信')
        self.payjs_key = config['payjs_key']   #填写通信密钥
        self.mchid = config['mchid'] #商户号
        self.host_api = 'https://payjs.cn/api/'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}

    def create_order(self,name,out_trade_no,total_price):
        order = {
            'body'         : name,  # 订单标题
            'out_trade_no' : out_trade_no,    # 订单号
            'total_fee'    : total_price,     # 金额,单位:分
            'mchid' : self.mchid            
        }
        order['sign'] = self.sign(order)

        
        r = requests.post(self.host_api+'/native',data=order,headers=self.headers)
        if r:
            print(r.json())
            return r #或qrcode;payjs_order_id等
        return False

    # 构造签名函数
    def sign(self,attributes):
        attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
        return hashlib.md5((unquote(urlencode(attributes_new))+'&key='+self.payjs_key).encode(encoding='utf-8')).hexdigest().upper()



    def check(self,payjs_order_id):     #这里是上一步主动生成的订单，单独调用
        order = {
            'payjs_order_id'    : payjs_order_id
        }
        order['sign'] = self.sign(order,self.payjs_key)

        r = requests.post(self.host_api+'/check',data=order,headers=self.headers)        
        try:
            if r.json()['status'] == '1':
                print(r.json())
                return True            
        except:
            return False
        return False
        
payjs = Payjs()