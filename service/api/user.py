from os import pardir
from time import time
from flask import Blueprint, request, jsonify, redirect, url_for
from flask import config
from flask import json
from service.database.models import Payment, ProdInfo,Config,Order,Message,Config,AdminUser
from service.api.db import db

#调用支付接口
from service.util.pay.alipay.alipayf2f import alipay    #支付宝接口
from service.util.pay.hupijiao.xunhupay import Hupi     #虎皮椒支付接口
from service.util.pay.codepay.codepay import codepay    #码支付
from service.util.pay.payjs.payjs import payjs  #payjs接口

from service.util.order.handle import make_order
#异步操作
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

#日志记录
from service.util.log import log
import bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

base = Blueprint('base', __name__,url_prefix='/api/v2')

#用户访问界面
@base.route('/')
def index():
    return 'base hello'


@base.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        user = AdminUser.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404
        
        # if bcrypt.checkpw(password.encode('utf-8'), user.hash):
        if bcrypt.checkpw(password.encode('utf-8'), user.hash.encode('utf-8')):
            access_token = create_access_token(identity={"email": email})
            return {"access_token": access_token}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


@base.route('/home', methods=['get'])
def home():
    # 系统信息
    # 前端需求：logo地址；footer信息，顶部公告；全局弹窗公告；加载公告
    try:
        infos = Config.query.filter().all()
    except Exception as e:
        log(e)
        return '数据库异常', 500
    return jsonify([x.to_json() for x in infos])

@base.route('/theme_list', methods=['get'])
def theme_list():
    info= {}
    # 系统信息
    # from service.database.models import Config
    # # 商品列表
    # 商品列表：【f按分类排除结果】
    # from service.database.models import ProdInfo
    try:
        prods = ProdInfo.query.filter_by(isactive = 1).all()
    except Exception as e:
        log(e)
        return '数据库异常', 500    
    prod_list =[x.to_json() for x in prods]
    tmp_cags = []
    num_list = []
    num = -1
    for x in prod_list:
        if x['cag_name'] not in tmp_cags:
            tmp_cags.append(x['cag_name'])
            num +=1
        num_list.append(num)    
    shop_list = []
    for x,i in enumerate(tmp_cags):
        goods = {}
        goods['cag_name'] = i    #大分类
        shops = []
        for y,n in enumerate(num_list): #y为位置，n为值
            if x == n:
                shops.append(prod_list[y])
        goods['shops'] = shops
        shop_list.append(goods)
    info['shops'] = shop_list   
    return jsonify(info)

@base.route('/detail/<int:shop_id>', methods=['get'])
def detail(shop_id):
    try:
        prod = ProdInfo.query.filter_by(id = shop_id).first_or_404('Product not exist')
    except Exception as e:
        log(e)
        return '数据库异常', 500       
    return jsonify(prod.detail_json())

@base.route('/get_order', methods=['post']) #已售订单信息
def get_order():
    contact = request.json.get('contact',None)
    if not contact:
        return '参数丢失', 404
    try:
        orders = Order.query.filter_by(contact = contact).all()
    except Exception as e:
        log(e)
        return '数据库异常', 500          
    return jsonify([x.admin_json() for x in orders])   


@base.route('/get_pay_list', methods=['get'])
def get_pay_list():
    try:
        pays =  Payment.query.filter_by(isactive = True).all()
    except Exception as e:
        log(e)
        return '数据库异常', 500        
    
    # return jsonify({'pays':['支付宝当面付','码支付微信','PAYJS支付宝'],'icons':['支付宝当面付','码支付微信','PAYJS支付宝']})
    return jsonify([x.enable_json() for x in pays])


@base.route('/get_pay_url', methods=['post'])
def get_pay_url():
    name = request.json.get('name',None).replace('=','_')  #防止k，v冲突
    out_order_id = request.json.get('out_order_id',None)
    total_price = request.json.get('total_price',None)
    payment = request.json.get('payment',None)
    if payment not in ['支付宝当面付','虎皮椒微信','虎皮椒支付宝','码支付微信','码支付支付宝','码支付QQ','PAYJS支付宝','PAYJS微信']:
        return '暂无该支付接口', 404
    if not all([name,out_order_id,total_price]):
        return '参数丢失', 404        
    if payment == '支付宝当面付':
        try:
            ali_order = alipay.api_alipay_trade_precreate(
                subject=name,
                out_trade_no=out_order_id,
                total_amount=total_price,
                notify_url=None
            )
        except Exception as e:
            log(e)
            return '支付宝处理失败', 504                
        # print(ali_order)
        if ali_order['code'] == '10000' and ali_order['msg'] == 'Success':
            return jsonify(ali_order)   #默认自带qrcode
        return '调用支付接口失败', 400
    elif payment == '虎皮椒微信':
        try:
            obj = Hupi()
            pay_order = obj.Pay(trade_order_id=out_order_id,total_fee=total_price,title=name)
        except Exception as e:
            log(e)
            return '数据库异常', 500                
        # print(ali_order)
        if pay_order.json()['errmsg'] == 'success!':
            """
            {'openid': 20205992711,
            'url_qrcode': 'https://api.xunhupay.com/payments/wechat/qrcode?id=20205992711&nonce_str=5073110106&time=1603170015&appid=201906121518&hash=2c079048857dde2da83c740d9dcf3ad0',
            'url': 'https://api.xunhupay.com/payments/wechat/index?id=20205992711&nonce_str=7001051163&time=1603170015&appid=201906121518&hash=9a0192253f1f502e0bff6da77540c4ee',
            'errcode': 0,
            'errmsg': 'success!',
            'hash': '2d63d86e7b405ab34ac28204ba77d6d6'}
            """
            return jsonify({'qr_code':pay_order.json()['url']})
        return '调用支付接口失败', 400
    elif payment == '虎皮椒支付宝':
        obj = Hupi(payment='alipay')
        try:
            pay_order = obj.Pay(trade_order_id=out_order_id,total_fee=total_price,title=name)
        except Exception as e:
            log(e)
            return '数据库异常', 500                        
        
        # 参数错误情况下，会失效
        if pay_order.json()['errmsg'] == 'success!':
            return jsonify({'qr_code':pay_order.json()['url']})
        return '调用支付接口失败', 400
    elif payment == '码支付微信' or '码支付支付宝' or '码支付QQ':
        # 参数错误情况下，会失效
        try:
            qr_url = codepay.create_order(payment,total_price,out_order_id)
        except Exception as e:
            log(e)
            return '数据库异常', 500                        
        return jsonify({'qr_code':qr_url})
    elif payment == 'PAYJS支付宝' or 'PAYJS微信':
        # 参数错误情况下，会失效
        try:
            r = payjs.create_order(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '数据库异常', 500                        
        return jsonify({'qr_code':r.json()['code_url'],'payjs_order_id':r.json()['payjs_order_id']})        
    else:
        return '开发中', 400


## 本地检测--》尝试改为服务器检测，避免用户支付过程退出页面

@base.route('/check_pay', methods=['post']) #检测状态或取消订单
def check_pay():
    # print(request.json)
    out_order_id = request.json.get('out_order_id',None)
    methord = request.json.get('methord',None)
    payment = request.json.get('payment',None) #支付方式
    #其余订单信息
    name = request.json.get('name',None) #
    contact = request.json.get('contact',None) #
    contact_txt = request.json.get('contact_txt',None) #备注
    price = request.json.get('price',None) #
    num = request.json.get('num',None) #
    total_price = request.json.get('total_price',None) #
    if methord not in ['check','cancel']:
        return '请求方法不正确', 400
    if not out_order_id:
        return '参数丢失', 404
    if not all([name,contact,price,num,total_price]):
        return '参数丢失2',400
    # 支付渠道校验
    if payment == '支付宝当面付':
        if methord == 'check':
            try:
                result = alipay.api_alipay_trade_query(out_trade_no=out_order_id)
            except Exception as e:
                log(e)
                return '支付宝请求错误', 500                
            
            # print(result)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                start = time()
                # print('支付成功1')  #默认1.38s后台执行时间；重复订单执行时间0.01秒；异步后，时间为0.001秒
                # make_order(out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                # print('提交结果1')
                # print(time()-start) 
                return jsonify({'msg':'success'})
            return jsonify({'msg':'not paid'})  #支付状态校验        
        else:   #取消订单
            alipay.api_alipay_trade_cancel(out_trade_no=out_order_id)
            return jsonify({'msg':'订单已取消'})
    elif payment == '虎皮椒支付宝' or '虎皮椒微信':
        if methord == 'check':
            try:
                obj = Hupi()
                result = obj.Check(out_trade_order=out_order_id)
            except Exception as e:
                log(e)            
                return '虎皮椒请求错误', 502
            #失败订单
            try:
                if result.json()['data']['status'] == "OD":  #OD(支付成功)，WP(待支付),CD(已取消)
                    executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                    return jsonify({'msg':'success'})                
            except :
                return jsonify({'msg':'订单参数不正确'})

            return jsonify({'msg':'not paid'})  #支付状态校验        
        else:   #取消订单
            return jsonify({'msg':'订单已取消'})
    elif payment == '码支付微信' or '码支付支付宝' or '码支付QQ':
        if methord == 'check':
            result = codepay.check(out_order_id)
            #失败订单
            try:
                if result['msg'] == "success":  #OD(支付成功)，WP(待支付),CD(已取消)
                    executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                    return jsonify({'msg':'success'})                
            except :
                return jsonify({'msg':'订单参数不正确'})

            return jsonify({'msg':'not paid'})  #支付状态校验        
        else:   #取消订单
            return jsonify({'msg':'订单已取消'})     
    elif payment == 'PAYJS支付宝' or 'PAYJS微信':
        if methord == 'check':
            payjs_order_id = request.json.get('payjs_order_id',None)
            result = payjs.check(payjs_order_id)
            #失败订单
            try:
                if result:
                    executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                    return jsonify({'msg':'success'})                
            except :
                return jsonify({'msg':'订单参数不正确'})

            return jsonify({'msg':'not paid'})  #支付状态校验        
        else:   #取消订单
            return jsonify({'msg':'订单已取消'})                        
    else:
        return '开发中', 400




@base.route('/get_card', methods=['post']) #已售订单信息
def get_card():
    out_order_id = request.json.get('out_order_id',None)
    if not out_order_id:
        return '参数丢失', 404
    try:
        card = Order.query.filter_by(out_order_id = out_order_id).first_or_404()
    except Exception as e:
        log(e)            
        return '虎皮椒请求错误', 502        
    
    return jsonify(card.only_card())    #返回卡密和订单时间

@base.route('/success', methods=['get'])
def success():
    order_id = request.json.get('order_id',None)
    contact = request.json.get('contact',None)
    if not order_id and not contact:
        return '请输入订单或联系方式', 404
    if order_id:
        try:
            result = Order.query.filter_by(serial_id = order_id).first_or_404()
        except Exception as e:
            log(e)            
            return '订单请求失败', 502              
        
        return jsonify([result.to_json()])
    else:
        try:
            result = Order.query.filter_by(contact = contact).all()
        except Exception as e:
            log(e)            
            return '订单请求失败', 502              
        if result:
            return jsonify([r.to_json() for r in result])
        return '商品不存在或已过期', 404
    

    