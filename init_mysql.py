from service.database.models import creat_table,drop_table,AdminUser
from service.config.config import init_db
from service.api.db import db
# print(os.getenv('MYSQL_HOST'))
# print(os.getenv('MYSQL_PORT'))
# print(os.getenv('MYSQL_PASSWORD'))
# 初始化数据
import re
import random
import string

def new_table():
    # 清空表
    drop_table()
    # 创建表
    creat_table()
    # 初始化表
    init_db()    

def init():
    mod_key() # 熵增
    try:
        # res = bool(AdminUser.query.filter_by(id = 1).first())
        # res = AdminUser.query.get(1)    #主键查询
        res = AdminUser.query.filter_by(id = 1).one_or_none()
    except:
        # print(e)
        db.session.commit()
        res = False
    if res:
        print('检测到已存在数据库')
    else:
        try:
            new_table()
            print('新数据库初始化完成')   
        except Exception as e:
            print(e)
            print('初始化失败,请检查数据库设置、防火墙、以及是否初始化完成')

def ranstr(num):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))

def mod_key():
    w_str = ''
    randkey = ranstr(random.randint(44,48))
    flag = False
    with open('./service/api/db.py','r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if re.search('a44545de51d5e4deaswdedcecvrcrfr5f454fd1cec415r4f',line):
                line = re.sub('a44545de51d5e4deaswdedcecvrcrfr5f454fd1cec415r4f',randkey,line)
                flag = True
            w_str += line
    if flag:        
        with open('./service/api/db.py','w',encoding='utf-8') as f:
            f.write(w_str)

init()


