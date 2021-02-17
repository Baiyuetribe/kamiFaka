from urllib.parse import quote
from hashlib import md5

import requests
from service.util.pay.pay_config import get_config

class CodePay:
    CODEPAY_TYPE_ALIPAY = 1
    CODEPAY_TYPE_QQ = 2
    CODEPAY_TYPE_WECHAT = 3

    def __init__(self):
        # self.codepay_id = '58427'   #马支付ID
        # self.codepay_key = 'fgljhMdS34Sbo86Mn6Gk2mvmLpTRrmbn'   #码支付密钥
        # self.api_host = 'https://api.xiuxiu888.com/'
        self.api_host = 'http://api2.fateqq.com:52888/'

        # self.token = 'jljCGU3pRviAW64LqaHPjHIvdm05b1iq'     #网页自己设置的token
    #https://api.xiuxiu888.com/creat_order/?id=58427&token=fgljhMdS34Sbo86Mn6Gk2mvmLpTRrmbn&price=1&order_id=admin&type=2&page=3&pay_id=5454545
    #https://api.xiuxiu888.com/creat_order/?id=58427&token=fgljhMdS34Sbo86Mn6Gk2mvmLpTRrmbn&price=1&pay_id=admin&type=2&page=3
    def create_order(self, code_name, price, out_order_id, notify_url="", return_url="", param="",):
        if code_name == '码支付支付宝':
            codepay_type = 1
            config = get_config('码支付支付宝')
        elif code_name == '码支付微信':
            config = get_config('码支付微信')
            codepay_type = 3
        else:
            config = get_config('码支付QQ')
            codepay_type = 2
        data = {
            "id": config['codepay_id'],
            "pay_id": out_order_id,
            "type": codepay_type,
            "price": price,
            "notify_url": notify_url,
            "return_url": return_url,
            "param": param,
        }
        signs = ""
        urls = ""
        for k in sorted(data.keys()):
            v = data[k]
            if not isinstance(v, str):
                v = str(v)
            if not v or k == "sign":
                continue
            if signs:
                urls += "&"
                signs += "&"
            signs += f"{k}={v}"
            urls += f"{k}={quote(v.encode())}"
        sign = md5((signs + config['codepay_key']).encode()).hexdigest()
        query = f"{urls}&sign={sign}"
        url = f"{self.api_host}creat_order/?{query}"
        return {'qr_code':url}  #输出url地址
    #https://api.xiuxiu888.com/ispay?id=' + 用户ID + '&token=' + 随机token或MD5 + '&order_id=' + 订单唯一ID
    #http://api2.xiuxiu888.com/ispay?id=10041&order_id=17571427&token=888888&call=callback

    def check(self,out_order_id):
        config = get_config('码支付支付宝')
        url = f"{self.api_host}ispay/?id={config['codepay_id']}&order_id={out_order_id}&token={config['token']}"
        r = requests.get(url)
        #{'status': -1, 'msg': 'no'}    #{"status":-6,"msg":"token error"}
        if r.json()['msg'] == 'ok':
            return True
        return False
