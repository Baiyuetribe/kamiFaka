from os import name
from service.util.pay.hupijiao.xunhupay import payment
from service.database.models import Payment,Config

def get_config(name):
    if name == 'web_url':
        return Config.query.filter_by(name = 'web_url').first().info    #返回URL
    # 支付渠道名称
    return Payment.query.filter_by(name = name).first().all_json()['config']