from flask import make_response
from service.database.models import *
from service.api.db import db
import os
from shutil import copy
import time

BACKUP_PATH = os.path.join(os.path.dirname(__file__),'../../../public/backups')
ORIGIN_PATH = os.path.join(os.path.dirname(__file__),'../../../public')

# 重要信息：
# 支付设置备份
def payment_backup():
    # 输出名称、配置参数，txt格式==》支付宝当面付--？appid:xxxx;alipay_pub:xxxx;key:xxx
    txt = '\n【=====支付参数备份=====】'
    try:
        res = Payment.query.filter().all()
        for i in res:
            tmp = i.all_json()
            txt += '\n'+tmp['name']+'---激活状态：'+str(tmp['isactive'])
            txt += '\n---配置信息：' + str(tmp['config'])
        # print(txt)
        return txt
    except:
        return txt

# 邮箱设置
def smtp_backup():
    # 发件人、昵称、地址、端口、密码
    txt = '\n【=====邮箱参数备份=====】'
    try:
        tmp = Notice.query.filter_by(id = 1).first().to_json()['config']
        txt += '\n发件人邮箱:' + tmp['sendmail']
        txt += '\n发件人昵称:' + tmp['sendname']
        txt += '\nSMTP地址:' + tmp['smtp_address']
        txt += '\nSMTP端口:' + tmp['smtp_port']
        txt += '\n密码:' + tmp['smtp_pwd']
        return txt
    except:
        return txt        


# 消息通知
def notice_backup():
    # 管理员--邮箱、微信、tg、短信==开关；用户==开关
    txt = '\n【=====消息通知备份=====】'
    try:
        res = Notice.query.filter().all()
        tmps = [x.to_json() for x in res]
        for i in tmps:
            txt += '\n'+i['name']+'---管理员账号：'+i['admin_account']+'  管理员开关状态：'+str(i['admin_switch'])
        return txt
    except:
        return txt        


# 网址设置
def system_backup():
    # id,名称，内容
    txt = '\n【=====网站设置备份=====】'
    try:
        res = Config.query.filter().all()
        tmps = [x.to_json() for x in res]
        for i in tmps:
            txt += '\nID：'+str(i['id'])+'---名称：'+i['name']+'---描述：'+i['description']+'---具体内容：'+i['info']
        return txt
    except:
        return txt        

# 分类设置
def cag_backup():
    # 名称、描述、排序
    txt = '\n【=====商品分类备份=====】'
    try:
        res = ProdCag.query.filter().all()
        tmps = [x.to_json() for x in res]
        for i in tmps:
            txt += '\n分类名：'+ i['name']+'---描述：'+i['info']+'---排序值：'+str(i['sort'])
        return txt
    except:
        return txt        


# 商品设置
def shop_backup():
    # id,名称，分类，一句话描述，图片展示，排序，内容介绍，价格，发货模式，上线状态
    txt = '\n【=====商品备份=====】'
    try:
        res = ProdInfo.query.filter().all()
        tmps = [x.admin_edit() for x in res]
        for i in tmps:
            txt += '\n【'+ i['name']+'】---所属分类：'+i['cag_name']+'---一句话描述：'+i['info']+'---一展示图片：'+i['img_url']+'---一价格：'+str(i['price'])+'---发货模式：'+str(i['auto'])+'---是否上架：'+str(i['isactive'])
            txt += '\n------商品详细描述：'+i['discription']
        return txt
    except:
        return txt        

# 卡密信息
def card_backup():
    # 商品名称+是否重复，\n卡密信息，
    txt = '\n【=====卡密信息备份=====】'
    try:
        res = Card.query.filter_by(isused = False).all()
        tmps = [x.to_json() for x in res]
        prod_names = [] #暂存商品列表
        for i in tmps:
            if i['prod_name'] not in prod_names:
                prod_names.append(i['prod_name'])
                txt += '\n【'+ i['prod_name']+'】---是否重复：'+str(i['reuse'])+' 卡密信息：'
            txt += '\n'+str(i['card'])
        return txt
    except:
        return txt        

# 订单列表
def order_backup():
    # 此部分不支持再次导入。
    txt = '\n【=====订单信息备份=====】'
    try:
        txt = '<---  此部分导出后，升级不再支持导入 ---->'
        res = Order.query.filter().all()
        tmps = [x.admin_json2() for x in res]
        for i in tmps:
            txt += '\n订单时间:'+str(i['updatetime'])+'订单ID：'+ i['out_order_id']+'---【'+i['name']+'】---支付渠道:'+i['payment']+'---联系方式:'+str(i['contact'])+'---购买数量:'+str(i['num'])+'---总价格:'+str(i['total_price'])+'---卡密:'+str(i['card'])
        return txt
    except:
        return txt     
#路径设置
SQL_PATH = os.path.join(os.path.dirname(__file__),'../../public/sql')           
def order_backup_sql():
# def order_backup():
    from datetime import datetime
    # 此部分不支持再次导入。
    drop_order_table()  # 清空中间order表
    creat_order_table()
    # 初始化表
    res = Order.query.filter().all()
    orders = []
    for i in res:
        tmp = i.admin_json2()
        orders.append(Order2(tmp['out_order_id'],tmp['name'],tmp['payment'],tmp['contact'],tmp['contact_txt'],tmp['price'],tmp['num'],tmp['total_price'],tmp['card'],tmp['status'],datetime.strptime(tmp['updatetime'], "%Y-%m-%d %H:%M:%S")))
    try:
        db.session.add_all(orders)
        db.session.commit()
        return 'ok'
    except Exception as e:
        print(e)
    return 'ok'

def update_order():
    # 更新order订单列表
    try:
        db.session.query(Order).delete()
        db.session.commit()
    except Exception as e:
        print(e)
    # 清空后写入全新数据
    new_orders = []
    res = Order2.query.filter().all()
    for i in res:
        tmp = i.admin_json2()
        try:
            new_orders.append(Order(out_order_id=tmp['out_order_id'],name=tmp['name'],payment=tmp['payment'],contact=tmp['contact'],contact_txt=tmp['contact_txt'],price=tmp['price'],num=tmp['num'],total_price=tmp['total_price'],card=tmp['card'],status=tmp['status'],updatetime=datetime.strptime(tmp['updatetime'], "%Y-%m-%d %H:%M:%S")))
        except Exception as e:
            print(e)   
    try:
        db.session.add_all(new_orders)
        db.session.commit()
        return 'ok'
    except Exception as e:
        print(e)         
    return 'ok'



def get_time():
    return time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())

def create_dir(dir_path): #创建目录--->输入demo,会在BACKUP_PATH目录下新建demo文件夹，输入demo/abc==>目录下新建demo/adc文件夹
    dir_to_create = BACKUP_PATH +'/' +dir_path
    if not (os.path.exists(dir_to_create)):
        os.mkdir (dir_to_create)

def copyfile(src,dst):  #输入两个目录,
    for filename in os.listdir(src):
        file = os.path.join(src,filename)
        copy(file,dst)

## 静态资源备份--上传的图片
def images_backup():
    # 原样copy
    # 图片文件copy
    src = os.path.join(ORIGIN_PATH+'/images')
    # 目标文件创建
    create_dir('images')    #备份目录下创建图片文件夹
    dst = os.path.join(BACKUP_PATH+'/images')
    copyfile(src,dst)
    # 图片备份
    
# 数据库备份
def sql_backup():
    SQL_PATH = os.path.join(os.path.dirname(__file__),'../../../public/sql')
    src = SQL_PATH+'/kamifaka.db'
    create_dir('sql') 
    dst = os.path.join(BACKUP_PATH+'/sql')
    if os.path.exists(src):
        copy(src,dst)

def make_file(content,filename):
    res = make_response(content)
    res.headers["Content-Disposition"] = f"p_w_upload; filename={filename}.txt"
    return res

def loc_sys_back(): #系统信息备份

    # return make_file(payment_backup()+smtp_backup()+notice_backup()+system_backup(),'支付邮箱等系统信息')
    return payment_backup()+smtp_backup()+notice_backup()+system_backup()


def loc_shop_back(): #商品卡密备份
    # return make_file(cag_backup()+shop_backup()+card_backup(),'商品及卡密信息备份')
    return cag_backup()+shop_backup()+card_backup()

def loc_order_back(): #订单备份
    # return make_file(order_backup(),'订单导出')
    return order_backup()

def main_back():    # 服务器端备份
    #开始备份系统信息
    backup_time = get_time()
    with open(BACKUP_PATH+'/支付邮箱等系统备份'+backup_time+'.txt','w',encoding='utf-8') as f:
        f.write(payment_backup()+smtp_backup()+notice_backup()+system_backup()) #写入系统配置

    with open(BACKUP_PATH+'/商品分类等卡密备份'+backup_time+'.txt','w',encoding='utf-8') as f:
        f.write(cag_backup()+shop_backup()+card_backup()) #写入系统配置

    with open(BACKUP_PATH+'/历史订单信息备份'+backup_time+'.txt','w',encoding='utf-8') as f:
        f.write(order_backup()) #写入系统配置        
    
    # 文件操作
    images_backup()
    # 原始数据库 仅支持sqlite
    sql_backup()



## 输出目录==》public/backup/images + 系统配置.txt + 分类及商品信息。txt + 卡密信息.txt,文件标注日期避免冲突，图片覆盖或跳过