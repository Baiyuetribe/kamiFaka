import requests
import hashlib
from urllib.parse import urlencode,unquote


class Payjs(object):

    def __init__(self,payment='wechat'):
        self.payment = payment
        from service.util.pay.pay_config import get_config
        if payment == 'wechat':
            config = get_config('PAYJS微信')
        else:
            config = get_config('PAYJS支付宝')
        self.web_url = get_config('web_url')
        self.payjs_key = config['payjs_key']   #填写通信密钥
        self.mchid = config['mchid'] #商户号
        self.host_api = 'https://payjs.cn/api'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        
    def create_order(self,name,out_trade_no,total_price):
        order = {
            'body'         : name,  # 订单标题
            'attach':'kmfaka_'+self.payment,
            'out_trade_no' : out_trade_no,    # 订单号
            'total_fee'    : int(float(total_price)*100),     # 金额,单位:分
            'mchid' : self.mchid,
            'notify_url':self.web_url + '/notify/payjs'            
        }
        order['sign'] = self.sign(order)

        r = requests.post(self.host_api+'/native',data=order,headers=self.headers)
        try:
            if r and r.json()['return_msg'] == 'SUCCESS':
                return {'qr_code':r.json()['code_url'],'payjs_order_id':r.json()['payjs_order_id']}
                """
                {'code_url': 'weixin://wxpay/bizpayurl?pr=c60Vl0W00', 'out_trade_no': 'Order_1605517714455ggqrw0ka', 'payjs_order_id': '2020111617083400522394864', 'qrcode': 'https://payjs.cn/qrcode/d2VpeGluOi8vd3hwYXkvYml6cGF5dXJsP3ByPWM2MFZsMFcwMA==', 'return_code': 1, 'return_msg': 'SUCCESS', 'total_fee': '999', 'sign': 'B23C6619DE28827835A8BB501E425583'}
                """
        except:
            pass
        return False

    # 构造签名函数
    def sign(self,attributes):
        attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
        return hashlib.md5((unquote(urlencode(attributes_new))+'&key='+self.payjs_key).encode(encoding='utf-8')).hexdigest().upper()

    
    def sign2(self,attributes):
        attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
        sign_str = "&".join(
            [f"{key}={attributes_new[key]}" for key in attributes_new.keys()]
        )
        return (
            hashlib.md5((sign_str + "&key=" + self.payjs_key).encode(encoding="utf-8"))
            .hexdigest()
            .upper()
        )

    def check(self,payjs_order_id):     #这里是上一步主动生成的订单，单独调用
        order = {
            'payjs_order_id': payjs_order_id
        }
  
        order['sign'] = self.sign(order)
        r = requests.post(self.host_api+'/check',data=order,headers=self.headers)    
        try:
            if r.json()['status'] == 1:
                return True            
        except:
            return False
        return False
        
    def verify(self,data):     #异步通知    这里data=request.from
        try:
            signature = data['sign']
            data.pop('sign')
            return signature == self.sign2(data)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False    

# payjs = Payjs()