import json
import requests
import hashlib

class Mugglepay:
    def __init__(self):
        from service.util.pay.pay_config import get_config    
        config = get_config('Mugglepay')
        self.TOKEN = config['TOKEN']  # mugglepay密钥
        self.Currency= config['Currency']  # mugglepay密钥
        # self.RETURN_URL= config['Web_url']  # mugglepay地址
        self.web_url = get_config('web_url')

    def create_order(self,name,out_trade_no,total_price):
        header = {
            "token": self.TOKEN
        }
        data = {'merchant_order_id': out_trade_no, 'price_amount': total_price, 'price_currency': self.Currency, 'callback_url': self.web_url+'/notify/mugglepay',
                'title': name,'token':self.sign(out_trade_no)}
        # print(data)
        try:
            req = requests.post('https://api.mugglepay.com/v1/orders', headers=header, data=data)
            rst_dict = json.loads(req.text)
            # print(rst_dict)
            if rst_dict['status'] == 201:
                pay_url = rst_dict['payment_url']
                return {'qr_code':pay_url}
            return None
        except Exception as e:
            print(e)
            return None

    # 构造签名函数
    def sign(self,out_order_id):
        return hashlib.md5((out_order_id+self.TOKEN).encode(encoding='utf-8')).hexdigest().upper()


    def check(self,out_trade_no):
        header = {
            "token": self.TOKEN
        }
        try:
            req = requests.get('https://api.mugglepay.com/v1/orders/{}'.format(out_trade_no, ), headers=header)
            rst_dict = json.loads(req.text)
            # print(rst_dict)
            if rst_dict['status'] == 200:
                pay_status = str(rst_dict['order']['status'])
                if pay_status == 'PAID':
                    # print('支付成功')
                    return True
            return None
        except Exception as e:
            print(e)
            return None

    def verify(self,data):     #异步通知    这里data=request.from
        try:
            signature = data['token']
            out_order_id = data['merchant_order_id']
            return signature == self.sign(out_order_id)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False    
