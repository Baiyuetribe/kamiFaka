import requests
import hashlib
from urllib.parse import urlencode,unquote

class Ymq:

    def __init__(self,payment='wechat'):
        from service.util.pay.pay_config import get_config
        # config = get_config('随便付')
        self.web_url = get_config('web_url')
        if payment == 'wechat':
            config = get_config('云免签微信')
        else:
            config = get_config('云免签支付宝')
        self.payment = payment
        self.app_id = config['APP_ID'] #商户号
        self.key = config['KEY']
        self.API = 'https://open.yunmianqian.com/api/'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}

        
    def create_order(self,name,out_trade_no,total_price):
        data = {
            'app_id' : self.app_id,    # 商户ID
            'out_order_sn' : out_trade_no,    # 订单号
            'name' : name,   # 1跳转 2json 
            'pay_way' : self.payment,   # 个人收款码
            'price'    : int(total_price*100),     # 金额,单位:分
            'attach'    :'kmfaka',
            'notify_url':self.web_url + '/notify/ymq',
        }
        data['sign'] = hashlib.md5((data['app_id']+str(data['out_order_sn'])+str(data['name'])+str(data['pay_way']+str(data['price'])+str(data['attach'])+str(data['notify_url'])+self.key)).encode('utf8')).hexdigest()
        # print(urlencode(order))
        r = requests.post(self.API+'pay',data=data,headers=self.headers)
        # print(r.text)
        if r.status_code == 200:
            if r.json()['code'] == 200:
                res = r.json()['data']
                return {'qr_code':res['qr'],'payjs_order_id':res['out_order_sn'],'reallyPrice':res['pay_price']/100,'redirect':2}
        return False
    
    def sign(self,data):
        try:
            return hashlib.md5((data['app_id']+str(data['order_sn'])+str(data['out_order_sn'])+str(data['notify_count'])+str(data['pay_way']+str(data['price'])+str(data['qr_type'])+str(data['qr_price'])+str(data['pay_price'])+str(data['created_at'])+str(data['paid_at'])+str(data['attach'])+str(data['server_time'])+self.key)).encode('utf8')).hexdigest()
        except:
            return None
    def verify(self,data):     #异步通知    这里data=request.from
        try:
            signature = data['sign']
            data.pop('sign')
            return signature == self.sign(data)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False    

# payjs = Payjs()