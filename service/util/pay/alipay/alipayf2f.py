from alipay import AliPay
from alipay.utils import AliPayConfig

# app_private_key_string = open("/path/to/your/private/key.pem").read()
# alipay_public_key_string = open("/path/to/alipay/public/key.pem").read()

class AlipayF2F:

    def __init__(self):
        from service.util.pay.pay_config import get_config
        config = get_config('支付宝当面付')
        self.APPID = config['APPID']
        self.web_url = get_config('web_url')
        self.app_private_key_string = '-----BEGIN RSA PRIVATE KEY-----\n'+config['app_private_key']+'\n-----END RSA PRIVATE KEY-----'
        self.alipay_public_key_string = '-----BEGIN PUBLIC KEY-----\n'+config['alipay_public_key']+'\n-----END PUBLIC KEY-----'   
        self.alipay = AliPay(
            appid=self.APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=self.app_private_key_string,
            alipay_public_key_string=self.alipay_public_key_string,
            sign_type="RSA2", # RSA 或者 RSA2
            debug=False,  # True后为开发环境，所有走dev接口，正式环境用False
            config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
        )
    def create_order(self,name,out_order_id,total_price):
        # 注意加上开头结尾
        ali_order = self.alipay.api_alipay_trade_precreate(
            subject=name,
            out_trade_no=out_order_id,
            total_amount=total_price,
            notify_url=self.web_url + '/notify/alipay'
        )
        try:
            if ali_order['code'] == '10000' and ali_order['msg'] == 'Success':        
                return ali_order
        except Exception as e:
            print(e)
            pass
        return False

    def check(self,out_order_id):     #这里是上一步主动生成的订单，单独调用
        try:
            res = self.alipay.api_alipay_trade_query(out_trade_no=out_order_id)
            # print(res)
            if res.get("trade_status", "") == "TRADE_SUCCESS":
                return True
        except Exception as e:
            print(e)
            return False
        return False

    def verify(self,data):     #异步通知    这里data=request.from
        try:
            signature = data['sign']
            data.pop('sign')
            return self.alipay.verify(data,signature)   # 结果为一个布尔值
        except Exception as e:
            print(e)
            return False

    def cancle(self,out_order_id):
        try:
            self.alipay.api_alipay_trade_cancel(out_trade_no=out_order_id)
            return True
        except:
            return False






# #本地开发环境测试
# app_private_key_string = '-----BEGIN RSA PRIVATE KEY-----\n'+'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCqWmxsyPLwRmZHwoLYlUJXMF7PATKtvp7BrJfwLbxwrz6I48G11HpPPyAoNynwAMG7DCXjVX76NCbmfvvPqnbk09rNRULqGju8G6NkQTbLfDjhJs+CE8kdIs89btxqDG70ebePiZTGpQngPLfrziKDOhRfXkA5qRPImbC+PUXiXq9qvkp9Yu/8IYjyxUpNBNjZuTK+fTjSI0RCt7eE+wR0KqpNIzot1q/ds1KTIYmJQM5tEFie4BK0pDtGiIs/VrUG8PTPqLyzEyIMy1N75olUWAiGrk0USqiieP3TYj0PdlQDX2T14DOwMkl5Rjvt7Knc+WGdolPIBssUX1wTE+J7AgMBAAECggEAWpRP+Jv0yRu1wMxFRKJArxmSH+GUL9wej/6Un2nCO+yChMkNtAAxtLdtAtUqIGpWmH2CG9nW9XULhh3ZCPer1kprmiAMz2t5fbD4dRNT7miz2cwIJDMfCbX7mb+7xUutJ6Mcnl7aU7FnierfJKvrn/ke4gK8haxIT66g0tbDtPQhYnGPawyM+gqFulaMBcuqH0naAIq5ZBWHkKuuwJ1SD6yGrWgHdq3Kt2pE8b9yjfdUl15IeW0rszXG6fTika9WX6qaulyoGAAZdjiXED+mbRyqZA3jq7RI38qBP9+/jAb+fdwE8EwqnpPvfGHMBdkREOXK0kzRU8rpd9GbH7INaQKBgQDwpuW+bK/qxKx3BSAXL98f0J2I7YVuk0EFCStGoxnzWRv0yvL0QEDwN+QPiVMmcVQcr79mW5zTBkd4vmr3ud+v1f/X6UPI82kQhZlVWry8LEnisPlZuE0E/EaJrLgF7z4l3ItzCVi8IfpgizPcCYSz/vY49a5W34eKjXHWUB1jDwKBgQC1N8PgGKI2LRDaJeqt5Ef6yyYSMOgVe0WSqAlgyMECb1pjmMBjcNG1AFE/FfgNu4thOaXIogElGVoQFvA5GuJQY48HOJNgx3Ua2SxiowcXkAN0gIm4FY+ozkp7xhizvLVfsmX+MKqPtl6nggiWETJJyvMQnjMgKLmSvhsopMwZ1QKBgGV36az2BOK3VITGq3Y7YBf5DUN76uPpwOOPryiUgs+hhfEcVX55TSg8WLPYUjAGXtHNpKVTAXfU0PPvTgjv3Yo1cC+okkU7pNQrkLB1lti8z9Z+ilSzKf5tJIzOP7V437p1GHNDwJ9qsDhe2VnwxXxjh4wSwxSsIWlhJFuZ4hovAoGAFgm8Fmqof3InlH/79D3IyyUdciTkdIhTQ6yPx2dioYstMOOIsg8sUZjCSKvBSNo/7wj1slqRTROyMja37Bnq39/bqwMkWSaohSVYEn7FBAaNhQOEvBBTMjI0OK00n9cZL5QgdzMv6t5A0JottSJOPU8jFChJC2Yoe0IHR4ATGikCgYB2smi7/ptKiGdwmiuUHsF/U3jfjpHyHwLrXjoSU+mwV+GjqcdbtkSP1suGjN8tcdbFvLSCRX/IRdFHYJeuPUXQtZtiC431+upasbEiJ1xZ2KcK3lKf0mOn10kPD5QC7mmsfmjz4cw9cSrBjmcWGXeIwIXPLhOAAIzpHqy8oP/F/g=='+'\n-----END RSA PRIVATE KEY-----'

# alipay_public_key_string = '-----BEGIN PUBLIC KEY-----\n'+'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4AHTfGleo8WI3qb+mSWOjJRyn6Vh8XvO6YsQmJjPnNKhvACHTHcU+PCUWUKZ54fSVhMkFZEQWMtAGeOt3lGy3pMBS96anh841gxJc2NUljU14ESXnDn4QdVe4bosmYvfko46wfA0fGClHdpO8UUiJGLj1W5alv10CwiCrYRDtx93SLIuQgwJn4yBC1/kE/KENOaWaA45dXIQvKh2P0lTbm0AvwYMVvYB+eB1GtOGQbuFJXUxWaMa0byTo9wSllhgyiIkOH+HJ9oOZIweGlsrezeUUdr3EEX97k25LdnUt/oQK8FIfthexfWZpTDDlHqmI7p6gCtRVDJenU4sxwpEyQIDAQAB'+'\n-----END PUBLIC KEY-----'

# # 注意加上开头结尾

# alipay = AliPay(
#     appid="2016091800537528",
#     app_notify_url=None,  # 默认回调url
#     app_private_key_string=app_private_key_string,
#     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#     alipay_public_key_string=alipay_public_key_string,
#     sign_type="RSA2", # RSA 或者 RSA2
#     debug=True,  # True后为开发环境，所有走dev接口，正式环境用False
#     config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
# )

