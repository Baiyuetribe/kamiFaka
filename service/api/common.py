from flask import Blueprint, Response,request,jsonify
from flask import render_template,redirect,send_from_directory
import time
import os

from service.util.order.handle import notify_success

from flask.helpers import make_response
from service.util.pay.alipay.alipayf2f import   AlipayF2F
from service.util.pay.hupijiao.xunhupay import Hupi     #虎皮椒支付接口
from service.util.pay.codepay.codepay import CodePay    #码支付
from service.util.pay.payjs.payjs import Payjs  #payjs接口
from service.util.pay.wechat.weixin import Wechat   # 微信官方
from service.util.pay.qq.qqpay import QQpay   # 微信官方
from service.util.pay.epay.common import Epay   # 易支付
from service.util.pay.mugglepay.mugglepay import Mugglepay
from service.util.pay.yungouos.yungou import YunGou
from service.util.pay.vmq.vmpay import VMQ  # V免签
from service.util.pay.codepay.codepay import CodePay

common = Blueprint('common', __name__)
# common = Blueprint('common', __name__,static_folder='../../dist/static',template_folder='../../dist/admin')

# app = Flask(__name__,static_folder='../../dist/static',template_folder='../../dist')
def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

import time
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(10)

def timefn(fn):
    """计算性能的修饰器"""
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {t2 - t1: .5f} s")
        return result
    return measure_time

@common.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(common.root_path, '../../dist'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 图片公共路径
UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'../../public/images')



@common.route('/images/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_PATH,filename)

# def notify_success(out_order_id):
#     print(f'{out_order_id}订单处理完毕')

#前端
@common.route('/')
def index():
    # return '恭喜，后端部署成功'
    return render_template('index.html')
    # return """<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor:
    # pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family:
    # "Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal;
    # margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"><p>
    #  <br/><span style="font-size:30px">恭喜您,后端正常运行。</span></p></div> """
#管理员---当前访客与管理员共用一套系统；后期可尝试分割管理员部分，更小的缩减前端体积
@common.route('/admin')
def admin():
    # return '恭喜，后端部署成功'
    # return render_template('/admin/index.html')
    return render_template('admin.html')

@common.route('/login')
def login():
    return render_template('admin.html')

import xml.etree.ElementTree as ET


@common.route('/notify/<name>',methods=['POST','GET'])    #支付回调测试
def notify(name):
    # print('请求地址:'+ request.url)
    # print(request.form.to_dict()) #适用于post请求，但是回调时get请求
    # print(request.args)
    if name == 'alipay':
        trade_status = request.form.get('trade_status', None)
        if trade_status == 'TRADE_SUCCESS':
            res = AlipayF2F().verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('out_trade_no', None)
                executor.submit(notify_success,out_order_id)
        return 'success'
    elif name == 'wechat':
        try:
            xml = request.data
            array_data = {}
            root = ET.fromstring(xml)
            for child in root:
                value = child.text
                array_data[child.tag] = value
            return_code = array_data['return_code']
            if return_code == 'SUCCESS':
                res = Wechat().verify(array_data)
                if res:
                    out_order_id = array_data['out_trade_no']
                    executor.submit(notify_success,out_order_id)
        except:
            pass
    elif name == 'xunhupay':
        trade_status = request.form.get('status',None)
        if trade_status == 'OD':
            res = Hupi(payment='wechat').verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('trade_order_id', None)
                executor.submit(notify_success,out_order_id)
    elif name == 'payjs':
        trade_status = request.form.get('return_code',None)
        if trade_status == '1':
            res = Payjs().verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('out_trade_no', None)
                executor.submit(notify_success,out_order_id)
    elif name == 'vmq':
        out_order_id = request.args.get('payId', None)
        if out_order_id and len(out_order_id) == 27:
            res = VMQ(payment='wechat').verify(request.args.to_dict())
            if res:
                executor.submit(notify_success,out_order_id)
    elif name == 'epay':
        trade_status = request.form.get('trade_status', None)
        if trade_status == 'TRADE_SUCCESS':
            res = Epay().verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('out_trade_no', None)
                executor.submit(notify_success,out_order_id)
    elif name == 'yungou':
        code = request.form.get('code', None)
        if code == '1':
            res = YunGou().verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('outTradeNo', None)
                executor.submit(notify_success,out_order_id)
    elif name == 'yungouwx':
        code = request.form.get('code', None)
        if code == '1':
            res = YunGou(payment = 'wechat').verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('outTradeNo', None)
                executor.submit(notify_success,out_order_id)
    elif name == 'codepay':
        pay_type = request.form.get('type', None)
        if pay_type:
            if pay_type == '3':
                payment = 'wechat'
            elif pay_type == '2':
                payment = 'qqpay'
            elif pay_type == '1':
                payment = 'alipay'
            res = CodePay(payment).verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('pay_id', None)
                executor.submit(notify_success,out_order_id)
    elif name == 'qqpay':
        try:
            xml = request.data
            array_data = {}
            root = ET.fromstring(xml)
            for child in root:
                value = child.text
                array_data[child.tag] = value
            # print(array_data)
            trade_state = array_data['trade_state']
            if trade_state == 'SUCCESS':
                res = QQpay().verify(array_data)
                if res:
                    out_order_id = array_data['out_trade_no']
                    executor.submit(notify_success,out_order_id)
        except:
            pass
    elif name == 'mugglepay':
        status = request.form.get('status', None)
        if status and status == 'PAID':
            res = Mugglepay().verify(request.form.to_dict())
            if res:
                out_order_id = request.form.get('merchant_order_id')
                executor.submit(notify_success,out_order_id)
    else:
        pass

    return 'success'

# @common.route('/return',methods=['POST','GET'])    #支付回调测试
# def back():
#     print(request.json)
#     with open('return.log','a',encoding='utf=8') as f:
#         f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' ' + str(request.json))
#     return jsonify(request.json)

# @common.route('/demo')
# def demo():


#     return str(~tg_switch)



@common.route('/robots.txt')
def robots():
    return Response('User-agent: *\n' + 'Disallow: /images/', 200, headers={'Content-Type': 'text/plain'})
