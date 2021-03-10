import requests
import hashlib
from urllib.parse import urlencode,unquote

class Sbpay:

    def __init__(self,payment='wechat'):
        from service.util.pay.pay_config import get_config
        # config = get_config('随便付')
        self.web_url = get_config('web_url')
        if payment == 'wechat':
            self.pay_type_id = 1
        else:
            self.pay_type_id = 2
        self.mch_uid = '90' #商户号
        self.key = 'AGZZCZA6A0WjSXP6IRmHw9BUClJa1r3H'
        
    def create_order(self,name,out_trade_no,total_price):
        order = {
            'mch_uid' : self.mch_uid,    # 商户ID
            'mepay_type' : 2,   # 个人收款码
            'notify_url':self.web_url + '/notify/sbpay',
            'out_trade_no' : out_trade_no,    # 订单号
            'param' : name,   # 1跳转 2json 
            'pay_type_id' : self.pay_type_id,
            'return_type' : 2,   # 1跳转 2json 
            'return_url' : self.web_url,   # 1跳转 2json 
            'total_fee'    : total_price,     # 金额,单位:分
        }
        order['sign'] = self.sign(order)
        # print(urlencode(order))
        print('https://www.sbpay.cn/pay.html?'+urlencode(order))
        r = requests.get(url='https://www.sbpay.cn/pay.html?'+urlencode(order))
        if r.status_code == 200:
            if r.json()['code'] == 1:
                return {'qr_code':r.json['Qrcode_Url'],'reallyPrice':r['Total']}
        return False
    
    def sign(self,attributes):
        attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
        sign_str = "&".join(
            [f"{key}={attributes_new[key]}" for key in attributes_new.keys()]
        )
        print(sign_str)
        return (
            hashlib.md5((sign_str + self.key).encode(encoding="utf-8"))
            .hexdigest()
            # .upper()
        )
        
    def verify(self,data):     #异步通知    这里data=request.from
        try:
            signature = data['sign']
            data.pop('sign')
            return signature == self.sign2(data)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False    

# payjs = Payjs()