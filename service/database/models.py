from sqlalchemy.sql.sqltypes import Float
from service.api.db import db
from datetime import datetime
from sqlalchemy import Column,Integer,String,Boolean,Text,DateTime

# from service.database.count import count_card
#管理员
class AdminUser(db.Model):
    __tablename__ = 'admin_user'  #此行可有可无
    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String(50), nullable=False)
    hash = Column(String(100), nullable=False)   #存储密码
    updatetime = Column(DateTime, nullable=True,default=datetime.now())   #存储变更时间
    
    def __init__(self, email, hash):
        self.email = email
        self.hash = hash
    def to_json(self):
        return {
            'email': self.email,
        }
class AdminLog(db.Model):
    __tablename__ = 'admin_login_log'  # 登录日志
    id = Column(Integer, primary_key=True,autoincrement=True)
    ip = Column(String(100), nullable=False)
    updatetime = Column(DateTime, nullable=True,default=datetime.now())   #存储变更时间
    def __init__(self, ip):
        self.ip = ip

class Payment(db.Model):
    __tablename__ = 'payment'  # 支付
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False,unique=True)  #支付接口名称
    icon = Column(String(100), nullable=False)  #图标
    config = Column(Text)  #配置参数{}json
    info = Column(String(100))  #描述
    isactive = Column(Boolean, nullable=False,default=False)

    def __init__(self, name, icon, config,info, isactive):
        self.name = name
        self.icon = icon
        self.config = config
        self.info = info
        self.isactive = isactive
    def enable_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'isactive': self.isactive,
            'icon': self.icon,
        }
    def all_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'config': eval(self.config),
            'info': self.info,
            'isactive': self.isactive,
        }          
class ProdCag(db.Model):
    __tablename__ = 'prod_cag'  # 分类设置
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False,unique=True)  #名称
    info = Column(String(100), nullable=False,comment='描述')  #描述
    sort = Column(Integer, nullable=True,default=1000)  #排序id

    def __init__(self, name, info, sort):
        self.name = name
        self.info = info
        self.sort = sort

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'sort': self.sort,
        }

class ProdInfo(db.Model):
    __tablename__ = 'prod_info'  # 产品信息
    id = Column(Integer, primary_key=True,autoincrement=True)
    # cag_name = Column(String(50),ForeignKey('prod_cag.name'))  #关联后，无法update或删除
    cag_name = Column(String(50))  #关联测试
    name = Column(String(150), nullable=False,unique=True)  #
    info = Column(String(150), nullable=True)  #产品一句话描述
    img_url = Column(String(150), nullable=True) #主图
    sort = Column(Integer, nullable=True,default=1000)  #排序
    discription = Column(Text, nullable=True)  #完整描述
    price = Column(Float, nullable=False)  #价格
    price_wholesale = Column(String(150), nullable=True)  #折扣
    # iswholesale = Column(Text, nullable=False,default=False)  #是否启用折扣
    auto = Column(Boolean, nullable=False,default=False)  #手工或自动发货
    sales = Column(Integer, nullable=True,default=0)  #销量
    tag = Column(String(50), nullable=True,default='优惠折扣')  #标签
    isactive = Column(Boolean, nullable=False,default=False)   #激活为1

    def __init__(self, cag_name, name, info, img_url, sort, discription, price,price_wholesale, auto, sales, tag, isactive):
        self.cag_name = cag_name
        self.name = name
        self.info = info
        self.img_url = img_url
        self.sort = sort
        self.discription = discription
        self.price = price
        self.price_wholesale = price_wholesale
        self.auto = auto
        self.sales = sales
        self.tag = tag
        self.isactive = isactive
    def to_json(self):  #用于首页列表展示
        return {
            'cag_name': self.cag_name,
            'name': self.name,
            'prod_id': self.id,
            'price': self.price,
            'img_url': self.img_url,
            'auto': self.auto,
            'tag': self.tag,
            'sales': self.sales,
            'stock': self.__count_card__(self.name),    #库存信息，此处函数处理
        }
    def __count_card__(self,prod_name):
        count = Card.query.filter_by(prod_name = prod_name,isused = False).count()
        if count > 10:
            return '充足'
        elif count == 0:
            return '缺货'
        elif count == 1:
            #再次统计
            if Card.query.filter_by(prod_name = prod_name,reuse = 1).count():
                return '充足'
            return '少量'
        else:
            return '少量' 
    def admin_json(self):
        return {
            'cag_name': self.cag_name,
            'name': self.name,
            'prod_id': self.id,
            'price': self.price,
            'price_wholesale': self.price_wholesale,
            'auto': self.auto,
            'tag': self.tag,
            'stock': self.__count_card__(self.name),
            'sales': self.sales,
            'isactive': self.isactive,
        }
    def admin_edit(self):
        return {
            'id': self.id,
            'cag_name': self.cag_name,
            'name': self.name,
            'info': self.info,
            'img_url': self.img_url,
            'sort': self.sort,
            'discription': self.discription,
            'price': self.price,
            'price_wholesale': self.price_wholesale,
            'auto': self.auto,
            'tag': self.tag,
            'sales': self.sales,
            'isactive': self.isactive,
        }                 
    def detail_json(self):
        return {
            'name': self.name,
            'prod_id': self.id,
            'price': self.price,
            'price_wholesale': self.price_wholesale,
            'img_url': self.img_url,
            'auto': self.auto,
            'tag': self.tag,
            'discription': self.discription,
        }     
    # 批发价格设计
    # 9，10；9.9，8.8
    # 9，10-100，101；9.9，8.8，7.7 
    # 9，10-100，101-500，501；9.9，8.8，7.7,6.6
    
    # 9#9.9，8.8
    # 9，100#9.9，8.8，7.7 
    # 9，100，500#9.9，8.8，7.7,6.6    

class Order(db.Model):
    __tablename__ = 'order'  # 订单信息
    id = Column(Integer, primary_key=True,autoincrement=True)
    out_order_id = Column(String(50), nullable=False)  #订单ID
    name = Column(String(50), nullable=False)  #商品名
    payment = Column(String(50), nullable=False)  #支付渠道
    contact = Column(String(50)) #联系方式
    contact_txt = Column(Text, nullable=True)  #附加信息
    price = Column(Float, nullable=False)  #价格
    num = Column(Integer, nullable=False) #数量
    total_price = Column(Float, nullable=False) #总价
    card = Column(Text, nullable=True)    #卡密
    status = Column(Boolean, nullable=True,default=True)    #订单状态
    updatetime = Column(DateTime, nullable=True,default=datetime.now())  #交易时间

    def __init__(self, out_order_id, name, payment, contact, contact_txt, price, num, total_price, card):
        self.out_order_id = out_order_id
        self.name = name
        self.payment = payment
        self.contact = contact
        self.contact_txt = contact_txt
        self.price = price
        self.num = num
        self.total_price = total_price
        self.card = card
        self.status = self.__check_card(self.card)
    def __check_card(self,card):
        if card:
            return True
        return False
    def to_json(self):
        return {
            'out_order_id': self.out_order_id,
            'name': self.name,
            'payment': self.payment,
            'contact': self.contact,
            'total_price': self.total_price,
            'card': self.card,
            'updatetime': self.updatetime,
        }
    def admin_json(self):
        return {
            'out_order_id': self.out_order_id,
            'name': self.name,
            'payment': self.payment,
            'contact': self.contact,
            'contact_txt': self.contact_txt,
            'num': self.num,
            'total_price': self.total_price,
            'card': self.card,
            'updatetime': self.updatetime,
        }
    def only_card(self):
        return {
            'card': self.card,
            'updatetime': self.updatetime,
        }                
class Card(db.Model):
    __tablename__ = 'card'  # 卡密
    id = Column(Integer, primary_key=True,autoincrement=True)
    prod_name = Column(String(50), nullable=False)  #商品ID
    card = Column(Text, nullable=False)  #卡密
    reuse = Column(Boolean, nullable=True,default=False)  #是否重复使用
    isused = Column(Boolean, nullable=True,default=False)  #是否已用


    def __init__(self, prod_name, card,reuse, isused):
        self.prod_name = prod_name
        self.card = card
        self.reuse = reuse
        self.isused = isused
    def to_json(self):
        return {
            'id': self.id,
            'prod_name': self.prod_name,
            'card': self.card,
            'reuse': self.reuse,
            'isused': self.isused,
        }

class Config(db.Model):
    __tablename__ = 'config'  # 系统配置
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100), nullable=False,unique=True)  #变量名
    info = Column(Text, nullable=True)  #值
    description = Column(Text, nullable=False)  #描述
    isshow = Column(Boolean, nullable=False,default=False)  #描述
    updatetime = Column(DateTime, nullable=True,default=datetime.now())  #交易时间

    
    def __init__(self, name, info,description,isshow):
        self.name = name
        self.info = info
        self.description = description
        self.isshow = isshow

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'description': self.description,
        }        


class Message(db.Model):
    __tablename__ = 'message'  # 通知或文章存档
    id = Column(Integer, primary_key=True,autoincrement=True)
    option = Column(Boolean, nullable=False)  #开关0/1;true,false
    info = Column(Text, nullable=False,default=False)  #消息
    classfiy = Column(String(50), nullable=False,default=False)  #类似，顶部公告或弹窗公告
    updatetime = Column(Text, nullable=True,default=datetime.now())  #
    
    def __init__(self, option, info, classfiy):
        self.option = option
        self.info = info
        self.classfiy = classfiy
    def to_json(self):
        return {
            'classfiy': self.classfiy,
            'info': self.info,
            'option': self.option,
        }

class Notice(db.Model):
    __tablename__ = 'notice'  # 通知引擎
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False,unique=True)  #邮箱、微信、TG、短信
    config = Column(Text,nullable=False)  #配置参数{}json
    admin_account = Column(String(100), nullable=False,default=False)  #150000
    admin_switch = Column(Boolean, nullable=True,default=False)  #管理员开关
    user_switch = Column(Boolean, nullable=True,default=False)  #用户开关
    def __init__(self, name, config, admin_account, admin_switch,user_switch):
        self.name = name
        self.config = config
        self.admin_account = admin_account
        self.admin_switch = admin_switch
        self.user_switch = user_switch
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'config': eval(self.config),
            'admin_account': self.admin_account,
            'admin_switch': self.admin_switch,
            'user_switch': self.user_switch
        }

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_json(self):
        return {
            'username': self.username,
            'password': self.password,
        }

def drop_table():
    db.drop_all()

def creat_table():
    db.create_all()



