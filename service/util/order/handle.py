from service.database.models import Card, Notice,Order
from service.api.db import db
import re
#接口调用
from service.util.message.smtp import mail_to_user,mail_to_admin
from service.util.message.sms import sms_to_user,sms_to_admin
from service.util.message.weixin import wxpush
from service.util.message.tg import post_tg

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

#日志记录
from service.util.log import log
#创建订单--走数据库
def make_order(out_order_id,name,payment,contact,contact_txt,price,num,total_price):
    # print('后台正在创建卡密')
    #订单ID，商品名称，支付方式，联系方式、备注、单价、数量、总价
    ## 根据name查找对应的卡密信息。---卡密有重复
    # 为避免同一订单二次请求，判断是否重复
    if not Order.query.filter_by(out_order_id = out_order_id).count():
        status = True   #订单状态
        # 生成订单 --除了上述内容外，还需要卡密。
        result = Card.query.filter_by(prod_name = name,isused = False).first()  #此处可用用0，也可以用false
        if result:
            card = result.to_json()['card']
            reuse = result.to_json()['reuse']   #返回True或False
            if not reuse: #卡密状态修改
                Card.query.filter_by(id = result.to_json()['id']).update({'isused':True})
        else:
            card = None
            status = False
            # print('卡密为空')
            log(f'{contact}购买的{name}缺货，卡密信息为空')
        #订单创建
        try:
            new_order= Order(out_order_id,name,payment,contact,contact_txt,price,num,total_price,card)
            db.session.add(new_order)
            db.session.commit()
        except Exception as e:
            log(e)
            return '订单创建失败', 500         

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
            log(e)  #代表通知序列任务失败
              
        


# 任务检测【主要】
def task(data):
    # 卡密获取
    #data包含{订单ID、商品名、支付方式、联系方式、总价格、卡密、日期}
    try:
        notices = [x.to_json() for x in Notice.query.filter().all()]
    except Exception as e:
        log(e)
        return '订单创建失败', 500       
    # 管理员和用户开关判断
    for i in notices:      #如果是邮箱，外加一个；或者conig内容直接为邮箱内容，传递邮箱参数
        # print(i['name'])
        if i['user_switch']:
            #发送用户邮件
            # send_user(i['name'],i['config'],data)   #传递通知方式
            executor.submit(send_user,i['name'],i['config'],data)
        if i['admin_switch']:
            # send_admin(i['name'],i['config'],i['admin_account'],data)
            executor.submit(send_admin,i['name'],i['config'],i['admin_account'],data)
    # # 系统检测：邮箱开关、微信开关、短信开关
    # ## 再次检测管理员开关【接收开关】，用户个性化判断：手机--发短信；邮箱--发邮件

#订单通知--用户
def send_user(notice_name,config,data):    #通知途径+卡密数据#包含{订单ID、商品名、支付方式、联系方式、总价格、卡密、日期}
    #状态检查：邮箱、短信---函数：开关判断；发送开关校验==》用户订单信息校验
    # def 系统开关检测
    # def用户联系方式检测
    if notice_name == '邮箱通知':   #只有邮箱和短信
        if re.match('^1[34578]\d{9}$', data['contact']):
            pass
        else:
            try:
                mail_to_user(config,data)   #配置和订单信息
            except Exception as e:
                log(e)  #邮箱通知失败         
            
    else:
        if re.match('^1[34578]\d{9}$',data['contact']):
            try:
                sms_to_user(config,data)
            except Exception as e:
                log(e)  #邮箱通知失败                
            
    # === 执行具体的函数：比如邮箱或短信通知
#---管理员
def send_admin(notice_name,config,admin_account,data):  #通知途径+管理员接收账号+msg信息[data['contact']+data['name']订单名]
    # 系统开关检测：邮箱、短信、TG、微信
    # 具体执行
    if notice_name == '邮箱通知':
        try:
            mail_to_admin(config,admin_account,data)
        except Exception as e:
            log('邮箱通知失败 ')  #          
            log(e)  #通知失败           
    elif notice_name == '短信通知':
        try:
            sms_to_admin(config,admin_account,data)
        except Exception as e:
            log('短信通知失败 ')  #          
            log(e)  #通知失败              
    elif notice_name == '微信通知':
        try:
            wxpush(config,admin_account,data)      #该步骤需要处理下
        except Exception as e:
            log('微信通知失败 ')  #          
            log(e)  #通知失败             
        
    elif notice_name == 'TG通知':
        try:
            post_tg(config,admin_account,data)     #该步骤需要处理
        except Exception as e:
            log('TG通知失败 ')  #          
            log(e)  #通知失败             
    else:
        print('接口参数错误')
        log('接口参数错误')  #通知失败 




## 库存检测。首页第一步返回数商品检测（已上架产品）；挨个检测商品库存数量：根据商品名检索，求sum值，结果：if重复卡密--充足；else:sum>10充足，否则少量；sum为0时缺货
# 库存统计
# Card.query.filter_by(prod_name = '香港ID').count()  ==》3

# 卡密添加：单一卡密无限重复使用及开关。