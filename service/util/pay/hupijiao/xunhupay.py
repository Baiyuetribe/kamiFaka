# *-* coding: UTF-8 *-*

import hashlib
import time
import json
import requests
# import qrcode
from urllib.parse import urlencode, unquote_plus


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


class Hupi(object):
    def __init__(self, payment='wechat'):  # ！！！通知、回调、callback都不能留空
        from service.util.pay.pay_config import get_config
        self.web_url = get_config('web_url')
        if payment == 'wechat':
            config = get_config('虎皮椒微信')
        else:
            config = get_config('虎皮椒支付宝')
        self.appid = config['appid']  # 数据库返回微信的APPID和SECRET
        self.AppSecret = config['AppSecret']  # 数据库返回微信的APPID和SECRET
        # 支持两种API模式：api.xunhupay.com和、api.vrmrgame.com，admin.xunhupay.com不支持
        self.API = 'https://'+config['API']
        self.payment = payment
        self.notify_url = self.web_url + '/notify/xunhupay'

    def curl(self, data, url):
        data['hash'] = self.sign(data)
        # print(data)
        headers = {"Referer": self.web_url}  # 自己的网站地址
        r = requests.post(url, data=data, headers=headers)
        return r

    def sign(self, attributes):
        attributes = ksort(attributes)
        # print(attributes)
        m = hashlib.md5()
        # print(unquote_plus(urlencode(attributes)))
        m.update((unquote_plus(urlencode(attributes)) +
                 self.AppSecret).encode(encoding='utf-8'))
        sign = m.hexdigest()
        #sign = sign.upper()
        # print(sign)
        return sign

    def Pay(self, trade_order_id, total_fee, title):  # 订单编号，支付方式，价格，标题
        url = self.API+'/payment/do.html'
        data = {
            "version": "1.1",
            # "lang":"zh-cn",#
            "plugins": "kmfaka_"+self.payment,
            "appid": self.appid,
            "trade_order_id": trade_order_id,
            "payment": self.payment,
            # "is_app":"Y",#
            "total_fee": total_fee,
            "title": title,
            # "description":"",#
            "time": str(int(time.time())),
            "notify_url": self.notify_url,  # 回调URL（订单支付成功后，WP开放平台会把支付成功消息异步回调到这个地址上）
            # "return_url":self.return_url, #支付成功url(订单支付成功后，浏览器会跳转到这个地址上)
            # "callback_url":self.callback_url,#商品详情URL或支付页面的URL（移动端，商品支付失败时，会跳转到这个地址上）
            "nonce_str": str(int(time.time())),  # 随机字符串(一定要每次都不一样，保证请求安全)
        }
        pay_order = self.curl(data, url)
        try:
            if pay_order.json()['errmsg'] == 'success!':
                return {'qr_code': pay_order.json()['url']}
        except:
            pass
        return False

    def Check(self, out_trade_order):  # 回调检测
        url = self.API+'/payment/query.html'
        data = {
            "appid": self.appid,
            "out_trade_order": out_trade_order,
            "time": str(int(time.time())),
            "nonce_str": str(int(time.time())),  # 随机字符串(一定要每次都不一样，保证请求安全)
        }
        result = self.curl(data, url)
        if result.json()['data']['status'] == "OD":  # OD(支付成功)，WP(待支付),CD(已取消)
            return True
        return False

    def verify(self, data):  # 异步通知    这里data=request.from
        try:
            signature = data['hash']
            data.pop('hash')
            return signature == self.sign(data)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False


def payment():
    pass


if __name__ == "__main__":
    obj = Hupi()
    order_id = '45455154444441212'
    r = obj.Pay(order_id, "0.1", "test")
    print(r, r.text)
    print(r.json()["url"])
    print('='*15)
    c = obj.Check(out_trade_order=order_id)
    print(c.text)
