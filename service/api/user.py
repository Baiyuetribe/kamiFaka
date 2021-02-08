from service.tg.tg_faka import pay
from time import time
from flask import Blueprint, request, jsonify
from service.database.models import Payment, ProdInfo,Config,Order,Config,ProdCag
from datetime import datetime,timedelta

#调用支付接口
from service.util.pay.alipay.alipayf2f import AlipayF2F    #支付宝接口
from service.util.pay.hupijiao.xunhupay import Hupi     #虎皮椒支付接口
from service.util.pay.codepay.codepay import CodePay    #码支付
from service.util.pay.payjs.payjs import Payjs  #payjs接口
from service.util.pay.wechat.weixin import Wechat   # 微信官方
from service.util.pay.epay.common import Epay   # 易支付
from service.util.pay.mugglepay.mugglepay import Mugglepay
from service.util.pay.yungouos.yungou import YunGou 

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
    name = request.json.get('name',None)
    out_order_id = request.json.get('out_order_id',None)
    total_price = request.json.get('total_price',None)
    payment = request.json.get('payment',None)
    if payment not in ['支付宝当面付','虎皮椒微信','虎皮椒支付宝','码支付微信','码支付支付宝','码支付QQ','PAYJS支付宝','PAYJS微信','微信官方接口','易支付','Mugglepay','YunGouOS','YunGouOS_WXPAY']:
        return '暂无该支付接口', 404
    if not all([name,out_order_id,total_price]):
        return '参数丢失', 404
    name = name.replace('=','_')  #防止k，v冲突        
    if payment == '支付宝当面付':
        try:
            ali_order = AlipayF2F().create_order(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '支付宝处理失败', 504                
        if ali_order['code'] == '10000' and ali_order['msg'] == 'Success':
            return jsonify(ali_order)   #默认自带qrcode
        return '调用支付接口失败', 400
        # return jsonify({'qr_code':'455555555454deffffffff'})
    elif payment == '虎皮椒微信':
        try:
            obj = Hupi()
            pay_order = obj.Pay(trade_order_id=out_order_id,total_fee=total_price,title=name)
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
        except Exception as e:
            log(e)
            return '数据库异常', 500                
        # print(ali_order)
    elif payment == '虎皮椒支付宝':
        
        try:
            obj = Hupi(payment='alipay')
            pay_order = obj.Pay(trade_order_id=out_order_id,total_fee=total_price,title=name)
        except Exception as e:
            log(e)
            return '数据库异常', 500                        
        # 参数错误情况下，会失效
        if pay_order.json()['errmsg'] == 'success!':
            return jsonify({'qr_code':pay_order.json()['url']})
        return '调用支付接口失败', 400
    elif payment in ['码支付微信','码支付支付宝','码支付QQ']:
        # 参数错误情况下，会失效
        try:
            qr_url = CodePay().create_order(payment,total_price,out_order_id)
            print(qr_url)
        except Exception as e:
            log(e)
            return '数据库异常', 500                        
        return jsonify({'qr_code':qr_url})
    elif payment in ['PAYJS支付宝','PAYJS微信']:
        # 参数错误情况下，会失效
        try:
            r = Payjs().create_order(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '数据库异常', 500  
        if r and r.json()['return_msg'] == 'SUCCESS':
            return jsonify({'qr_code':r.json()['code_url'],'payjs_order_id':r.json()['payjs_order_id']})   
        return '调用支付接口失败', 400                    
    elif payment in ['微信官方接口']:
        try:
            r = Wechat().create_order(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '数据库异常', 500
        if r:
            return jsonify({'qr_code':r})      
        return '调用支付接口失败', 400    
    elif payment in ['易支付']:
        try:
            r = Epay().create_order(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '数据库异常', 500
        if r:
            return jsonify({'qr_code':r})      
        return '调用支付接口失败', 400            
    elif payment in ['Mugglepay']:
        try:
            r = Mugglepay().create_order(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '数据库异常', 500
        if r:
            return jsonify({'qr_code':r})      
        return '调用支付接口失败', 400        
    elif payment in ['YunGouOS']:   # 统一接口
        try:
            r = YunGou(payment='unity').create_order(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '数据库异常', 500
        if r:
            return jsonify({'qr_code':r})      
        return '调用支付接口失败', 400      
    elif payment in ['YunGouOS_WXPAY']:   # 微信接口
        try:
            r = YunGou().create_order_wxpay(name,out_order_id,total_price)
        except Exception as e:
            log(e)
            return '数据库异常', 500
        if r:
            return jsonify({'qr_code':r})      
        return '调用支付接口失败', 400                           
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
    auto = request.json.get('auto',None) #
    if methord not in ['check','cancel']:
        return '请求方法不正确', 400
    if not out_order_id:
        return '参数丢失', 404
    if not all([name,contact,price,num,total_price]):
        return '参数丢失2',400
    if int(num) >0:
        # 支付渠道校验
        if payment == '支付宝当面付':
            if methord == 'check':
                try:
                    r = AlipayF2F().check(out_order_id)
                except Exception as e:
                    log(e)
                    return '支付宝请求错误', 500                
                # res = True  #临时测试
                # print(result)
                if r:
                    # start = time()
                    # print('支付成功1')  #默认1.38s后台执行时间；重复订单执行时间0.01秒；异步后，时间为0.001秒
                    # make_order(out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                    executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                    # print('提交结果1')
                    # print(time()-start) 
                    return jsonify({'msg':'success'})
                return jsonify({'msg':'not paid'})  #支付状态校验        
            else:   #取消订单
                AlipayF2F().cancle(out_order_id)
                return jsonify({'msg':'订单已取消'})
        elif payment in ['虎皮椒支付宝','虎皮椒微信']:
            if methord == 'check':
                try:
                    if payment == '虎皮椒微信':
                        obj = Hupi()
                    else:
                        obj = Hupi(payment='alipay')
                    result = obj.Check(out_trade_order=out_order_id)
                except Exception as e:
                    log(e)            
                    return '虎皮椒请求错误', 502
                #失败订单
                try:
                    if result.json()['data']['status'] == "OD":  #OD(支付成功)，WP(待支付),CD(已取消)
                        executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                        return jsonify({'msg':'success'})                
                except :
                    return jsonify({'msg':'订单参数不正确'})

                return jsonify({'msg':'not paid'})  #支付状态校验        
            else:   #取消订单
                return jsonify({'msg':'订单已取消'})
        elif payment in ['码支付微信','码支付支付宝','码支付QQ']:
            if methord == 'check':
                result = CodePay().check(out_order_id)
                #失败订单
                try:
                    if result['msg'] == "success":  #OD(支付成功)，WP(待支付),CD(已取消)
                        executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                        return jsonify({'msg':'success'})                
                except :
                    return jsonify({'msg':'订单参数不正确'})

                return jsonify({'msg':'not paid'})  #支付状态校验        
            else:   #取消订单
                return jsonify({'msg':'订单已取消'})     
        elif payment in ['PAYJS支付宝','PAYJS微信']:
            if methord == 'check':
                payjs_order_id = request.json.get('payjs_order_id',None)
                result = Payjs().check(payjs_order_id)
                #失败订单
                try:
                    if result:
                        executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                        return jsonify({'msg':'success'})                
                except :
                    return jsonify({'msg':'订单参数不正确'})

                return jsonify({'msg':'not paid'})  #支付状态校验        
            else:   #取消订单
                return jsonify({'msg':'订单已取消'})   
        elif payment in ['微信官方接口']:
            try:
                r = Wechat().check(out_order_id)
            except Exception as e:
                log(e)
                return '数据库异常', 500
            if r:
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                return jsonify({'msg':'success'})     
            return jsonify({'msg':'not paid'})   
        elif payment in ['易支付']:
            try:
                r = Epay().check(out_order_id)
            except Exception as e:
                log(e)
                return '数据库异常', 500
            if r:
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                return jsonify({'msg':'success'})     
            return jsonify({'msg':'not paid'})            
        elif payment in ['Mugglepay']:
            try:
                r = Mugglepay().check(out_order_id)
            except Exception as e:
                log(e)
                return '数据库异常', 500
            if r:
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                return jsonify({'msg':'success'})     
            return jsonify({'msg':'not paid'})          
        elif payment in ['YunGouOS','YunGouOS_WXPAY']:
            try:
                if payment == 'YunGouOS_WXPAY':
                    r = YunGou().check(out_order_id)
                else:
                    r = YunGou(payment='unity').check(out_order_id)
            except Exception as e:
                log(e)
                return '数据库异常', 500
            if r:
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price,auto)
                return jsonify({'msg':'success'})     
            return jsonify({'msg':'not paid'})              
        else:
            return '开发中', 400
    return 'erro', 404



@base.route('/get_card', methods=['post']) #已售订单信息--自动查询
def get_card():
    out_order_id = request.json.get('out_order_id',None)
    if not out_order_id:
        return '参数丢失', 404
    try:
        card = Order.query.filter_by(out_order_id = out_order_id).first()
    except Exception as e:
        log(e)

        # time.sleep()      
        return '订单创建失败', 400        
    
    return jsonify(card.only_card())    #返回卡密和订单时间

# @base.route('/success', methods=['get'])    #订单查询接口
# @limiter.limit("5 per minute", override_defaults=False)
# def success():
#     order_id = request.json.get('order_id',None)
#     contact = request.json.get('contact',None)
#     if not order_id and not contact:
#         return '请输入订单或联系方式', 404
#     if order_id:
#         try:
#             result = Order.query.filter_by(serial_id = order_id).first_or_404()
#         except Exception as e:
#             log(e)            
#             return '订单请求失败', 502              
        
#         return jsonify([result.to_json()])
#     else:
#         try:
#             result = Order.query.filter_by(contact = contact).all()
#         except Exception as e:
#             log(e)            
#             return '订单请求失败', 502              
#         if result:
#             return jsonify([r.to_json() for r in result])
#         return '商品不存在或已过期', 404
    

@base.route('/get_system', methods=['get'])
def get_system():
    try:
        res = Config.query.filter().all()
        info = {}
        for i in [x.to_json() for x in res]:
            info[i['name']] = i
        return jsonify(info)
    except:
        return '数据库异常', 503
    