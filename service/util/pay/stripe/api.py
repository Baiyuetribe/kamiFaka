import stripe

class Stripe(object):
    def __init__(self,payment='wechat'):
        from service.util.pay.pay_config import get_config    
        if payment == 'wechat':
            self.types = 'wechat'
            config = get_config('Stripe微信')
        else:
            self.types = 'alipay'
            config = get_config('Stripe支付宝')
        self.key = config['key']  # sk_开头密钥
        self.currency= config['currency']  # 美元或人名币
        self.web_url = get_config('web_url')
        self.return_url = self.web_url+'/notify/stripe'

        

    def create_order(self,name,out_trade_no,total_price):
        try:
            res = stripe.Source.create(
                type=self.types,    # 或alipay
                currency=self.currency, # 货币单位
                redirect={
                    'return_url': self.return_url
                },
                amount=int(total_price*100),    #最低4元起步
                api_key=self.key
            )

            data  = res.to_dict_recursive()
            print(data)
            # 返回url值，数据库存储secret值
            if self.types == 'wechat':    # 不清楚是否可直接扫码
                qr_code = data['wechat']['qr_code_url']
            else:
                qr_code = data['redirect']['url']
            return {'qr_code':qr_code,'redirect':1,'signs':data['id']+data['client_secret']} # 第三方状态1；本地2
        except Exception as e:
            print(e)
        return None

    # def verify(self,data):     #异步通知  # 没有异步校验，仅仅比对数据库里的三个参数即可
    #     try:
    #         data['source']  # 根据此查询数据==》获取之前存储的client
    #         if data['client_secret'] == 数据库client_secret:
    #             return True
    #     except Exception as e:
    #         print(e)
    #     return False
