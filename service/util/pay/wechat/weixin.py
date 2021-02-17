from wechatpay import WeChatPay

class Wechat:

    def __init__(self):
        from service.util.pay.pay_config import get_config    
        config = get_config('微信官方接口')
        self.WECHAT_APPID = config['APPID']
        self.WECHAT_MCH_ID = config['MCH_ID']
        self.WECHAT_PAY_SECRET = config['APP_SECRET']
        self.WECHAT_NOTIFY_URL = 'your_notify_url'
        # self.WECHAT_CERT = 'path/to/your_cert.pem'
        # self.WECHAT_KEY = 'patch/to/your_key.pem'
        self.pay = WeChatPay(self.WECHAT_APPID, self.WECHAT_MCH_ID,self.WECHAT_NOTIFY_URL, self.WECHAT_PAY_SECRET)
        # self.pay = super(Wechat,self.obj)

    def create_order(self,name,out_trade_no,total_fee): # total_fee为str，需要转换
        # print(type(total_fee))
        r = self.pay.unifiedorder(body=name,out_trade_no=out_trade_no,total_fee=int(float(total_fee)*100),spbill_create_ip='127.0.0.1')
        res = dict(r.result)
        if res['return_code'] == 'SUCCESS' and res['result_code'] == 'SUCCESS':
            return {'qr_code':res['code_url']}
        return None
        # {'return_code': 'SUCCESS',
        # 'return_msg': 'OK',
        # 'appid': 'xxxxxxx',
        # 'mch_id': 'xxxxxxxxx',
        # 'device_info': 'WEB',
        # 'nonce_str': 'sgwK0A4olzy6ZHx0',
        # 'sign': 'F4042EEB427B359D075030DAC439BDC0',
        # 'result_code': 'SUCCESS',
        # 'prepay_id': 'wx03204624526199f39ea6310946fad10000',
        # 'trade_type': 'NATIVE',
        # 'code_url': 'weixin://wxpay/bizpayurl?pr=hBAbIv700'}            
    
    def check(self,out_trade_no):
        # 查询订单
        r = self.pay.query_order(out_trade_no=out_trade_no)
        res = dict(r.result)
        if res['result_code'] == 'SUCCESS' and res['trade_state'] == 'SUCCESS':
            return True
        return False


    # OrderedDict([('return_code', 'SUCCESS'),
    #             ('return_msg', 'OK'),
    #             ('appid', 'wx861f5da31262aedf'),
    #             ('mch_id', '1525759081'),
    #             ('device_info', 'WEB'),
    #             ('nonce_str', 'Kdyr5MWIRVeLNfSl'),
    #             ('sign', 'A2E2D2BEB5F042822F1623FA09226FD1'),
    #             ('result_code', 'SUCCESS'),
    #             ('total_fee', '900'),
    #             ('out_trade_no', '445545d4e54dfefef54e54f65'),
    #             ('trade_state', 'NOTPAY'),
    #             ('trade_state_desc', '订单未支付')])        
    def cancel(self,out_trade_no):
        # 关闭交易
        r = self.pay.close_order(out_trade_no=out_trade_no)
        res = dict(r.result)
        if res['return_code'] == 'SUCCESS':
            return True
        return False


