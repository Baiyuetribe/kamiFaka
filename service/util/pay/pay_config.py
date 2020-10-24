from os import name
from service.util.pay.hupijiao.xunhupay import payment
from service.database.models import Payment

def get_config(name):
    # 支付渠道名称
    return Payment.query.filter_by(name = name).first().all_json()['config']