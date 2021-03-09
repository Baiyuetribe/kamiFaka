import requests
import hashlib
from urllib.parse import urlencode,unquote
import random
import string
import xml.etree.ElementTree as ET

class QQpay:

    def __init__(self):
        from service.util.pay.pay_config import get_config
        config = get_config('QQ钱包')
        self.web_url = get_config('web_url')
        self.host_api = 'https://qpay.qq.com/cgi-bin/pay/qpay_unified_order.cgi'    #https://qpay.qq.com/cgi-bin/pay/qpay_unified_order.cgi
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.key = config['key']
        self.mch_id = config['mch_id']
        
        
    def create_order(self,name,out_trade_no,total_price):
        order = {
            'mch_id'         : self.mch_id,  
            'nonce_str'         : ''.join(random.sample(string.ascii_letters + string.digits, 8)),  # 订单标题
            'body'         : name,  # 订单标题
            'out_trade_no' : out_trade_no,    # 订单号
            'total_fee'    : int(float(total_price)*100),     # 金额,单位:分
            'spbill_create_ip'         : '.'.join('%s'%random.randint(0, 255) for i in range(4)),  # 终端ip
            'notify_url':self.web_url + '/notify/qqpay',            
            'trade_type'         : 'NATIVE',  #
        }
        order['sign'] = self.sign(order)
        r = requests.post(self.host_api+'/native',data=order,headers=self.headers)
        if r.status_code == 200:
            xml = r.text
            array_data = {}
            root = ET.fromstring(xml)
            for child in root:
                value = child.text
                array_data[child.tag] = value
            if array_data['return_code'] == 'SUCCESS':
                return {'qr_code':array_data['code_url']}        
        return False

    # 构造签名函数
    def sign(self,attributes):
        attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
        return hashlib.md5((unquote(urlencode(attributes_new))+'&key='+self.key).encode(encoding='utf-8')).hexdigest().upper()

    # def check(self,payjs_order_id):     #这里是上一步主动生成的订单，单独调用
    #     order = {
    #         'payjs_order_id': payjs_order_id
    #     }
  
    #     order['sign'] = self.sign(order)
    #     r = requests.post(self.host_api+'/check',data=order,headers=self.headers)    
    #     try:
    #         if r.json()['status'] == 1:
    #             return True            
    #     except:
    #         return False
    #     return False
        
    def verify(self,data):     #异步通知    这里data=request.from
        try:
            signature = data['sign']
            data.pop('sign')
            return signature == self.sign(data)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False    

# payjs = Payjs()