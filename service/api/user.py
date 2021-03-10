from operator import concat
from time import time
from flask import Blueprint, request, jsonify
from service.database.models import Payment, ProdInfo,Config,Order,Config,ProdCag,TempOrder
from datetime import datetime,timedelta

from service.util.order.create import make_pay_url,make_tmp_order,check_pay_status


from service.util.order.handle import make_order
#异步操作
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

#日志记录
from service.util.log import log
from service.api.db import limiter

base = Blueprint('base', __name__,url_prefix='/api/v2')

#用户访问界面
@base.route('/')
def index():
    return 'base hello'

@base.route('/theme_list', methods=['get'])
def theme_list():
    info= {}
    # 系统信息
    try:
        prods = ProdInfo.query.filter_by(isactive = True).order_by(ProdInfo.sort).all()
        cags = ProdCag.query.filter().order_by(ProdCag.sort).all()
    except Exception as e:
        log(e)
        return '数据库异常', 503    
    prod_list =[x.to_json() for x in prods]
    cag_list = [x.to_json()['name'] for x in cags]
    tmp_cags = []
    for x in prod_list:
        if {'cag_name':x['cag_name'],'shops':[]} not in tmp_cags:
            tmp_cags.append({'cag_name':x['cag_name'],'shops':[]})
    sub_num = {}
    for index,i in enumerate(tmp_cags):
        sub_num[i['cag_name']] = index
    for i in prod_list:
        tmp_cags[sub_num[i['cag_name']]]['shops'].append(i)        
    new_cags = []
    for i in cag_list:
        for x in tmp_cags:
            if x['cag_name'] == i:
                new_cags.append(x)
    info['shops'] = new_cags   
    info['shops2'] = prod_list
    # 主题
    res = Config.query.filter_by(name = 'theme').first()
    info['theme'] = res.to_json()['info']
    return jsonify(info)

@base.route('/detail/<int:shop_id>', methods=['get'])
def detail(shop_id):
    try:
        prod = ProdInfo.query.filter_by(id = shop_id).first_or_404('Product not exist')
    except Exception as e:
        log(e)
        return '数据库异常', 503   
    res = prod.detail_json()
    try:
        if len(res['price_wholesale']) >5:
            price = res['price_wholesale'].split('#')[1]
            num = res['price_wholesale'].split('#')[0]
            prices = price.split(',')
            # 处理数量列表
            nums = []
            temp = num.split(',')
            s = len(temp)
            if s == 1:
                nums.append('1~'+temp[0])
                nums.append(str(int(temp[0])+1)+'~')
            elif s == 2:
                nums.append('1~'+temp[0])
                nums.append(str(int(temp[0])+1)+'~'+temp[1])
                nums.append(str(int(temp[1])+1)+'~')
            elif s == 3:
                nums.append('1~'+temp[0])
                nums.append(str(int(temp[0])+1)+'~'+temp[1])
                nums.append(str(int(temp[1])+1)+'~'+temp[2])
                nums.append(str(int(temp[2])+1)+'~')
            else:
                pass
            res['pifa'] = {'nums':nums,'prices':prices,'slice':temp}
    except:
        pass
    return jsonify(res)

@base.route('/get_order', methods=['POST']) #已售订单信息--废弃手机号或邮箱查询功能
@limiter.limit("5 per minute", override_defaults=False)
def get_order():
    # print(request.json)
    # print(request.args)
    contact = request.json.get('contact',None)
    # contact = request.args.get('contact',None)
    if not contact:
        return '参数丢失', 404
    try:
        orders = Order.query.filter_by(contact = contact).all()
    except Exception as e:
        log(e)
        return '数据库异常', 503   
    if orders:
        order = orders[-1].check_card() # {}
        time_count = datetime.utcnow()+timedelta(hours=8)-datetime.strptime(order['updatetime'],'%Y-%m-%d %H:%M') 
        if time_count.days:
            return 'not found', 200
        else:
            if time_count.seconds < 7200:
                return jsonify(order)
    return 'not found', 200


@base.route('/get_pay_url', methods=['post'])
@limiter.limit("10/minute;20/hour;40/day", override_defaults=False)
def get_pay_url():  # 传递名称、支付方式、订单号，购买数量，联系方式---》推算价格
    out_order_id = request.json.get('out_order_id',None)
    name = request.json.get('name',None)
    payment = request.json.get('payment',None)
    contact = request.json.get('contact',None)
    contact_txt = request.json.get('contact_txt',None)
    num = request.json.get('num',None)
    if payment not in ['支付宝当面付','虎皮椒微信','虎皮椒支付宝','码支付微信','码支付支付宝','码支付QQ','PAYJS支付宝','PAYJS微信','微信官方接口','易支付','Mugglepay','YunGouOS','YunGouOS_WXPAY','V免签微信','V免签支付宝','QQ钱包']:
        return '暂无该支付接口', 404
    if not all([name,out_order_id,contact,num]):
        return '参数丢失', 404
    num = int(num) 
    if num < 1:
        return '数量不正确', 404
    if len(out_order_id) != 27:
        return '不支持的订单号', 404
    # 创建临时订单
    r = make_tmp_order(out_order_id,name,payment,contact,contact_txt,num)
    if r:
        return jsonify(r)
    return '调用支付接口失败', 400

## 本地检测--》尝试改为服务器检测，避免用户支付过程退出页面
@base.route('/check_pay', methods=['post']) #检测状态或取消订单
@limiter.limit("6/minute;20/hour;40/day", override_defaults=False)
def check_pay():
    # print(request.json)
    out_order_id = request.json.get('out_order_id',None)
    payment = request.json.get('payment',None) #支付方式
    payjs_order_id = request.json.get('payjs_order_id',None) #支付方式
    if not out_order_id:
        return '参数丢失', 404
    if payment not in ['支付宝当面付','虎皮椒微信','虎皮椒支付宝','码支付微信','码支付支付宝','码支付QQ','PAYJS支付宝','PAYJS微信','微信官方接口','易支付','Mugglepay','YunGouOS','YunGouOS_WXPAY','V免签微信','V免签支付宝','QQ钱包']:
        return '暂无该支付接口', 404
    # 订单校验
    if TempOrder.query.filter_by(out_order_id = out_order_id,status = True).first():
        return jsonify({'msg':'success'})
    return jsonify({'msg':'not paid'})  #支付状态校验            
    # if check_pay_status(payment,out_order_id,payjs_order_id):
    #     return jsonify({'msg':'success'})
    # return jsonify({'msg':'not paid'})  #支付状态校验    

@base.route('/get_card', methods=['post']) #已售订单信息--自动查询
def get_card():
    out_order_id = request.json.get('out_order_id',None)
    if not out_order_id:
        return '参数丢失', 404
    try:
        card = Order.query.filter_by(out_order_id = out_order_id).first()
        if card:
            return jsonify(card.only_card())    #返回卡密和订单时间
    except Exception as e:
        log(e)
        # time.sleep()      
        return '订单创建失败', 400        
    
    return '订单丢失', 404
    

@base.route('/get_system', methods=['get'])
def get_system():
    try:
        res = Config.query.filter().all()
        info = {}
        for i in [x.to_json2() for x in res]:
            info[i['name']] = i
        pays =  Payment.query.filter_by(isactive = True).all()
        info['pays'] = [x.enable_json() for x in pays]  # ({'pays':['支付宝当面付','码支付微信','PAYJS支付宝'],'icons':['支付宝当面付','码支付微信','PAYJS支付宝']})
        return jsonify(info)
    except:
        return '数据库异常', 503
    