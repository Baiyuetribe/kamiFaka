import hashlib
from collections import OrderedDict
import requests

class YunGou:
    def __init__(self,payment='wechat'):
        from service.util.pay.pay_config import get_config    
        if payment == 'wechat':
            config = get_config('YunGouOS_WXPAY')
        else:
            config = get_config('YunGouOS')

        self.API = 'https://api.pay.yungouos.com/api/pay/merge/nativePay'   # 统一接口
        self.CHECK_API = 'https://api.pay.yungouos.com/api/system/order/getPayOrderInfo'
        self.WEIXIN_API = 'https://api.pay.yungouos.com/api/pay/wxpay/nativePay'    # 微信
        self.mch_id = config['mch_id']   # 商户号
        self.pay_secret = config['pay_secret']  # 商户密钥
    def _gen_sign(self, dct):
        """
        :param dct: 所需发送的所有数据的字典集合
            与微信官方一致
        :return: 签名
        """
        params = OrderedDict(sorted(dct.items(), key=lambda t: t[0]))
        stringA = ''
        for key, value in params.items():
            stringA += str(key) + '=' + str(value) + '&'
        stringSignTemp = stringA + 'key=' + self.pay_secret
        # print(stringSignTemp)
        # stringSignTemp = stringA + 'key=7b3515d618d2f0ae70f6ac453983ea7e'  # send box
        return hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()    

    def create_order(self,name,out_trade_no,total_fee): # total_fee为str，需要转换
        # print(type(total_fee))
        data = {
            'out_trade_no': out_trade_no,
            'total_fee': total_fee,
            'body': name,
            'mch_id': self.mch_id,
            # 'type': 2,  # 返回二维码
        }
        
        data.update({
            'sign': self._gen_sign(data)
        })        
        r = requests.post(self.API,data)
        if r.json()['code'] == 0:
            return {'qr_code':r.json()['data']}  #用于生成二维码付款
        return None

    def create_order_wxpay(self,name,out_trade_no,total_fee): # total_fee为str，需要转换
        # print(type(total_fee))
        data = {
            'out_trade_no': out_trade_no,
            'total_fee': total_fee,
            'body': name,
            'mch_id': self.mch_id,
            # 'type': 2,  # 返回二维码
        }
        
        data.update({
            'sign': self._gen_sign(data)
        })        
        r = requests.post(self.WEIXIN_API,data)
        if r.json()['code'] == 0:
            return {'qr_code':r.json()['data']} #用于生成二维码付款
        return None    
    
    def check(self,out_trade_no):
        # 查询订单
        data = {
            'out_trade_no': out_trade_no,
            'mch_id': self.mch_id,
            # 'type': 2,  # 返回二维码
        }     
        data.update({
            'sign': self._gen_sign(data)
        })          
        try:   
            r = requests.get(self.CHECK_API,data)
            if r.json()['data']['payStatus'] == 1:
                return True
            return None
        except:
            return None
  