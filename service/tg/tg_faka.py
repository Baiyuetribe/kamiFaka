import time
import io
import random
import string
import qrcode
import telegram
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ConversationHandler,CommandHandler,CallbackQueryHandler,MessageHandler,Filters,Updater
from service.database.models import Order,Plugin,ProdInfo,Payment,Card,Notice
from service.api.db import db

#调用支付接口
from service.util.pay.alipay.alipayf2f import AlipayF2F    #支付宝接口
from service.util.pay.hupijiao.xunhupay import Hupi     #虎皮椒支付接口
from service.util.pay.codepay.codepay import CodePay    #码支付
from service.util.pay.payjs.payjs import Payjs  #payjs接口

from service.util.message.smtp import mail_to_admin
from service.util.message.sms import sms_to_admin
from service.util.message.weixin import wxpush
from service.util.message.tg import post_tg

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

def get_config():
    result = Plugin.query.filter_by(name = 'TG发卡').first()
    if result:
        switch = result.to_json()['switch']
        about = result.to_json()['about']
        TOKEN = result.to_json()['config']['TG_TOKEN']
        if switch:
            if len(TOKEN) == 46:
                return TOKEN,about,switch
    return None    

ROUTE, PAYMENT,SUBMIT ,CHECK_PAY, PRICE, TRADE,  = range(6)

def make_qr_code(text):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # 字节转换
    qr_bytes = io.BytesIO()
    img.save(qr_bytes, format='PNG')
    return io.BytesIO(qr_bytes.getvalue())  #输入二进制

def start(update, context):
    if update.effective_user.username:
        keyboard = [
            [InlineKeyboardButton("购买商品", callback_data=str('购买商品')),   #前面为tg显示参数，后面为返回数据
             InlineKeyboardButton("查询订单", callback_data=str('查询订单')),
             InlineKeyboardButton("联系我们", callback_data=str('联系我们'))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            '请选择：',
            reply_markup=reply_markup
        )
        return ROUTE
    else:
        update.message.reply_text('请先设置TG用户名后再购买卡密')

def buy(update, context):
    query = update.callback_query
    query.answer()    
    # 给出商品列表，下一步给出支付方式、二维码弹出
    # shop_list = ['商品A','商品B','商品C',]  # 现货商品；包含名称、价格、库存、发货模式
    # shop_lists = [{'name':'商品A','price':9.9,'kucun':'充足','auto':'自动'},{'name':'商品B','price':9.9,'kucun':'充足','auto':'自动'},{'name':'商品C','price':9.9,'kucun':'充足','auto':'自动'}]  # 现货商品；包含名称、价格、库存、发货模式
    prods = ProdInfo.query.filter_by(isactive = True).all()
    prod_list =[x.admin_json() for x in prods] # 分类、名称、价格、是否自动发货，stock库存

    keyboard = []
    for i in prod_list:
        card_model = '手工发货'
        if i['auto']:
            card_model = '自动发货'
        shop_list = [InlineKeyboardButton(f"{i['name']}    价格：{str(i['price'])}￥  库存：{str(i['stock'])}  {card_model}", callback_data=str(i['name'])+'#'+str(i['price'])+'#'+str(i['stock']))]
        keyboard.append(shop_list)
    
    if len(keyboard) == 0:
        query.edit_message_text(text="商品都卖完了，请联系管理员补库存 主菜单: /start \n")
        return ConversationHandler.END        
    else:
        # 订单处理
        # 消息发送
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="请选择您要购买的商品：\n",
            reply_markup=reply_markup)
        return PAYMENT

def payment(update, context):
    # 给出支付方式，返回二维码+取消按钮
    query = update.callback_query
    query.answer()       
    call_data = query.data.split('#')
    if call_data[2] == '0':
        query.edit_message_text(text="该商品已缺货，请联系管理员补货: /start \n")
        return ConversationHandler.END            
    print(call_data)
    # 商品支付
    context.user_data['name'] = call_data[0] #商品名
    context.user_data['price'] = call_data[1] #商品名
    # print(context.user_data)

    pays =  Payment.query.filter_by(isactive = True).all()
    keyboard = []
    for i in pays:
        payment_list = [InlineKeyboardButton(f"{i.enable_json()['icon']}", callback_data=str(i.enable_json()['name']))] # InlineKeyboardButton("支付宝", callback_data=str('支付宝'))
        keyboard.append(payment_list)
    
    if len(keyboard) == 0:
        query.edit_message_text(text="暂无支付渠道，请联系管理员开启支付渠道: /start \n")
        return ConversationHandler.END        
    else:
        # 订单处理
        # 消息发送
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="请选择一种付款渠道：\n",
            reply_markup=reply_markup)
        return SUBMIT    

def pay(update, context):
    query = update.callback_query
    query.answer()       
    context.user_data['payment'] = query.data #获得支付方式
    context.user_data['contact'] = query.effective_user.id  # 下单CHAT_ID
    context.user_data['contact_txt'] = query.effective_user.username #下单用户名
    context.user_data['out_order_id'] = 'TG_'+str(int(time.time()))+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(14))  #len27
    


    # print(context.user_data)
    # 二维码输出
    #
    # qr_code_url = 'https://baiyue.one'
    result = get_pay_url(context.user_data)
    # print(result)
    if result:
        if query.data in ['PAYJS支付宝','PAYJS微信']:
            qr_code_url = result[0]
            context.user_data['payjs_order_id'] = result[1]
        else:
            qr_code_url = result
        query.edit_message_text(text='请在1分30s内完成支付，超时自动取消')
        bot = telegram.Bot(token=get_config()[0])
        bot.send_photo(chat_id=update.effective_user.id,photo=make_qr_code(qr_code_url))
        # 开启订单查询
        executor.submit(check_order,context.user_data)
        return CHECK_PAY
    else:
        query.edit_message_text(text="获取支付二维码失败 主菜单: /start \n")
    return ConversationHandler.END            

def get_pay_url(data):  # name,total_price,payment
    name = data['name']
    total_price= data['price']
    payment = data['payment']
    out_order_id = data['out_order_id']
    name = name.replace('=','_')  #防止k，v冲突        
    if payment == '支付宝当面付':
        try:
            ali_order = AlipayF2F().create_order(name,out_order_id,total_price)
        except Exception as e:
            print(e)
            return None
        if ali_order['code'] == '10000' and ali_order['msg'] == 'Success':
            return   ali_order['qr_code'] #默认自带qrcode
        return None
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
                return pay_order.json()['url']
            return None             
        except Exception as e:
            print(e)
            return None               
        # print(ali_order)

        
    elif payment == '虎皮椒支付宝':
        
        try:
            obj = Hupi(payment='alipay')
            pay_order = obj.Pay(trade_order_id=out_order_id,total_fee=total_price,title=name)
        except Exception as e:
            print(e)
            return None                       
        # 参数错误情况下，会失效
        if pay_order.json()['errmsg'] == 'success!':
            return pay_order.json()['url']
        return None  
    elif payment in ['码支付微信','码支付支付宝','码支付QQ']:
        # 参数错误情况下，会失效
        try:
            qr_url = CodePay().create_order(payment,total_price,out_order_id)
            # print(qr_url)
        except Exception as e:
            print(e)
            return None                      
        return qr_url
    elif payment in ['PAYJS支付宝','PAYJS微信']:
        # 参数错误情况下，会失效
        try:
            r = Payjs().create_order(name,out_order_id,total_price)
        except Exception as e:
            print(e)
            return None  
        if r and r.json()['return_msg'] == 'SUCCESS':
            return r.json()['code_url'],r.json()['payjs_order_id']
        return None                    
             
    else:
        return None 


def check_pay(data):
    # 查询接口
    out_order_id = data['out_order_id']
    payment = data['payment']
    #其余订单信息
    name = data['name']
    contact = data['contact']
    contact_txt = data['contact_txt']
    total_price = data['price']
    # 支付渠道校验
    if payment == '支付宝当面付':
        try:
            res = AlipayF2F().check(out_order_id)
        except Exception as e:
            print(e)
            return None              
        # res = True  #临时测试
        # print(result)
        if res:
            # start = time()
            # print('支付成功1')  #默认1.38s后台执行时间；重复订单执行时间0.01秒；异步后，时间为0.001秒
            # make_order(out_order_id,name,payment,contact,contact_txt,price,num,total_price)
            executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price=total_price,num=1,total_price=total_price)
            # print('提交结果1')
            # print(time()-start) 
            return True
        return None    
    elif payment in ['虎皮椒支付宝','虎皮椒微信']:
        try:
            obj = Hupi()
            result = obj.Check(out_trade_order=out_order_id)
        except Exception as e:
            print(e)            
            return None
        #失败订单
        try:
            if result.json()['data']['status'] == "OD":  #OD(支付成功)，WP(待支付),CD(已取消)
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                return True             
        except :
            return None
        return None    
      
    elif payment in ['码支付微信','码支付支付宝','码支付QQ']:
        result = CodePay().check(out_order_id)
        #失败订单
        try:
            if result['msg'] == "success":  #OD(支付成功)，WP(待支付),CD(已取消)
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                return True              
        except :
            return None
        return None        
    elif payment in ['PAYJS支付宝','PAYJS微信']:
        payjs_order_id = data['payjs_order_id']
        result = Payjs().check(payjs_order_id)
        #失败订单
        try:
            if result:
                executor.submit(make_order,out_order_id,name,payment,contact,contact_txt,price,num,total_price)
                return True             
        except :
            return None

        return None     
                       
    else:
        return None


#创建订单--走数据库
# def make_order(out_order_id,name,payment,contact,contact_txt,price,num,total_price):
def make_order(data):   # 主要为订单创建，异步一个管理员通知
    # print('后台正在创建卡密')
    out_order_id = data['out_order_id']
    name = data['name']
    payment = data['payment']
    contact = data['contact']
    contact_txt = data['contact_txt']
    price = data['price']
    num = 1
    total_price = price
    if not Order.query.filter_by(out_order_id = out_order_id).count():
        status = True   #订单状态
        # 生成订单 --除了上述内容外，还需要卡密。
        
        result = Card.query.filter_by(prod_name = name,isused = False).first()  #此处可用用0，也可以用false
        if result:
            card = result.to_json()['card']
            reuse = result.to_json()['reuse']   #返回True或False
            if not reuse: #卡密状态修改
                Card.query.filter_by(id = result.to_json()['id']).update({'isused':True})
                db.session.commit()
        else:
            card = None
            status = False
            # print('卡密为空')
            print(f'{contact}购买的{name}缺货，卡密信息为空')
            return None


        #订单创建
        try:
            # print(f'卡密信息{card}')
            new_order= Order(out_order_id,name,payment,contact,contact_txt,price,num,total_price,card)
            db.session.add(new_order)
            db.session.commit()
            # log('订单创建完毕')
        except Exception as e:
            print(e)
            # return '订单创建失败', 500    
            return None     

        ##构造data数据
        data = {}
        data['out_order_id'] = out_order_id
        data['name'] = name
        data['payment'] = payment
        data['contact'] = contact
        data['contact_txt'] = contact_txt
        data['price'] = price
        data['num'] = num
        data['total_price'] = total_price
        data['card'] = card
        data['status'] = status
        # 执行队列任务
        # print('后台正在执行队列')
        try:
            task(data)  #为避免奔溃，特别设置
        except Exception as e:
            print(e)  #代表通知序列任务失败                                
        



# 任务检测【主要】
def task(data):
    # 卡密获取
    #data包含{订单ID、商品名、支付方式、联系方式、总价格、卡密、日期}
    message = f"============\n订单号：{data['out_order_id']}\n商品名：{data['name']}\n时间：{data['updatetime']}\n订单内容：{data['card']}\n============\n"
    send_tg_msg(chat_id=data['contact'],message=message)
    try:
        notices = [x.to_json() for x in Notice.query.filter().all()]
    except Exception as e:
        print(e)
        return '订单创建失败', 500       
    # 管理员和用户开关判断
    for i in notices:      #如果是邮箱，外加一个；或者conig内容直接为邮箱内容，传递邮箱参数
        # print(i['name'])
        if i['user_switch']:
            #发送用户邮件
            # send_user(i['name'],i['config'],data)   #传递通知方式
            pass
            # executor.submit(send_user,i['name'],i['config'],data)
        if i['admin_switch']:
            # send_admin(i['name'],i['config'],i['admin_account'],data)
            executor.submit(send_admin,i['name'],i['config'],i['admin_account'],data)
    # # 系统检测：邮箱开关、微信开关、短信开关
    # ## 再次检测管理员开关【接收开关】，用户个性化判断：手机--发短信；邮箱--发邮件

def send_tg_msg(chat_id,message):
    bot = telegram.Bot(token=get_config()[0])
    bot.send_message(chat_id=chat_id,text=message)    
    # === 执行具体的函数：比如邮箱或短信通知
#---管理员
def send_admin(notice_name,config,admin_account,data):  #通知途径+管理员接收账号+msg信息[data['contact']+data['name']订单名]
    # 系统开关检测：邮箱、短信、TG、微信
    # 具体执行
    if notice_name == '邮箱通知':
        try:
            mail_to_admin(config,admin_account,data)
        except Exception as e:
            # log('邮箱通知失败 ')  #          
            print(e)  #通知失败           
    elif notice_name == '短信通知':
        try:
            sms_to_admin(config,admin_account,data)
        except Exception as e:
            # log('短信通知失败 ')  #          
            print(e)  #通知失败              
    elif notice_name == '微信通知':
        try:
            # print('微信通知')
            wxpush(config,admin_account,data)     
        except Exception as e:
            # log('微信通知失败 ')  #          
            print(e)  #通知失败             
        
    elif notice_name == 'TG通知':
        try:
            post_tg(config,admin_account,data)    
        except Exception as e:
            # log('TG通知失败 ')  #          
            print(e)  #通知失败             
    else:
        print('接口参数错误')
        # log('接口参数错误')  #通知失败 


def check_order(data):
    # 订单查询- 给出卡密信息
    # 上一步获得商品名称+支付渠道；用户id+昵称；商品里还有价格等属性
    # 先判断数据库是否存在订单，不存在则检查，存在则给出结果
    # 支付状态检查： 循环
    for i in range(88):
        time.sleep(4)
        # 支付后的效果
        if check_pay(data):
            break 

def trade_query(update, context):
    # trade_id = update.message.text
    # update.message.reply_text('请先设置TG用户名后再购买卡密')
    # print(update.effective_user)    # {'id': 472835979, 'first_name': '😛 定制脚本|网站搭建|故障维护', 'is_bot': False, 'username': 'Latte_Coffe', 'language_code': 'zh-hans'}
    
    chat_id = update.effective_user.id
    query = update.callback_query
    query.answer()
    print(query.data)
    # update.message.reply_text('期待再次见到你～')
    return ROUTE
    # if trade_list is None:
    #     update.message.reply_text('订单号有误，请确认后输入！')
    #     return ConversationHandler.END
    # elif trade_list[10] == 'locking':
    #     goods_name, description, trade_id = trade_list[2], trade_list[3], trade_list[0]
    #     update.message.reply_text(
    #         '*订单查询成功*!\n'
    #         '订单号：`{}`\n'
    #         '订单状态：*已取消*\n'
    #         '原因：*逾期未付*'.format(trade_id),
    #         parse_mode='Markdown',
    #     )
    #     return ConversationHandler.END
    # elif trade_list[10] == 'paid':
    #     trade_id, goods_name, description, use_way, card_context = \
    #         trade_list[0], trade_list[2], trade_list[3], trade_list[4], trade_list[6]
    #     update.message.reply_text(
    #         '*订单查询成功*!\n'
    #         '订单号：`{}`\n'
    #         '商品：*{}*\n'
    #         '描述：*{}*\n'
    #         '卡密内容：`{}`\n'
    #         '使用方法：*{}*\n'.format(trade_id, goods_name, description, card_context, use_way),
    #         parse_mode='Markdown',
    #     )
    #     return ConversationHandler.END

def search_order(update, context):  #done
    query = update.callback_query
    query.answer()        
    chat_id = update.effective_user.id  #用于查询订单
    user_name = update.effective_user.username
    # print(chat_id)  # 472835979

    orders = Order.query.filter_by(contact = chat_id).limit(5).all()
    
    # order_txt = [{'name':'shopA','card':'xxxxxxx','date':'2020:12:1'},{'name':'shopB','card':'xxxxxxx','date':'2020:12:1'}]

    if len(orders) == 0:
        query.edit_message_text(text="订单不存在: /start \n")
    else:
        order_info = f'您好{user_name},您最近的{str(len(orders))}个订单内如下：\n============\n'
        for i in orders:
            order_info += f"订单号：{i.check_card()['out_order_id']}\n商品名：{i.check_card()['name']}\n时间：{i.check_card()['updatetime']}\n订单内容：{i.check_card()['card']}\n============\n"
        
        query.edit_message_text(text=order_info)

    return ConversationHandler.END

def about(update, context): #done
    query = update.callback_query
    query.answer()
    # html_txt = "### 联系我们简介"
    html_txt = get_config()[1]
    query.edit_message_text(text=html_txt,parse_mode='Markdown')
    return ConversationHandler.END 

def cancel(update, context):
    update.message.reply_text('期待再次见到你～')
    return ConversationHandler.END

def timeout(update, context):
    update.message.reply_text('会话超时，期待再次见到你～ /start')
    return ConversationHandler.END

start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ROUTE: [
                CommandHandler('start', start),
                CallbackQueryHandler(buy, pattern='^' + str('购买商品') + '$'),
                CallbackQueryHandler(search_order, pattern='^' + str('查询订单') + '$'),
                CallbackQueryHandler(about, pattern='^' + str('联系我们') + '$'),
            ],
            PAYMENT: [
                CommandHandler('start', start),
                CallbackQueryHandler(payment, pattern='.*?'),
            ],  
            SUBMIT: [
                CommandHandler('start', start),
                CallbackQueryHandler(pay, pattern='.*?'),
                CallbackQueryHandler(cancel, pattern='^' + str('取消订单') + '$')
            ],    
            CHECK_PAY: [
                CommandHandler('start', start),
                CallbackQueryHandler(payment, pattern='.*?'),
            ],                                
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.all, timeout)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )


def run_bot():
    config = get_config()
    # print(config)
    if config:
        updater = Updater(token=config[0], use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(start_handler)
        # dispatcher.add_handler(admin_handler)
        updater.start_polling()
        updater.idle()


