import json
import requests

class Mugglepay:
    def __init__(self):
        from service.util.pay.pay_config import get_config    
        config = get_config('Mugglepay')
        self.TOKEN = config['TOKEN']  # mugglepay密钥
        self.Currency= config['Currency']  # mugglepay密钥
        self.RETURN_URL= config['Web_url']  # mugglepay地址

    def create_order(self,name,out_trade_no,total_price):
        header = {
            "token": self.TOKEN
        }
        data = {'merchant_order_id': out_trade_no, 'price_amount': total_price, 'price_currency': self.Currency, 'success_url': self.RETURN_URL,
                'title': name}
        # print(data)
        try:
            req = requests.post('https://api.mugglepay.com/v1/orders', headers=header, data=data)
            rst_dict = json.loads(req.text)
            if rst_dict['status'] == 201:
                pay_url = rst_dict['payment_url']
                return pay_url
            return None
        except Exception as e:
            print(e)
            return None


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

