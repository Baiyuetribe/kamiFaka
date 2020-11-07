import os
from service.database.models import creat_table,drop_table,AdminUser
from service.config.config import init_db
# print(os.getenv('MYSQL_HOST'))
# print(os.getenv('MYSQL_PORT'))
# print(os.getenv('MYSQL_PASSWORD'))
# 初始化数据

def new_table():
    # 清空表
    drop_table()
    # 创建表
    creat_table()
    # 初始化表
    init_db()    

def init():
    try:
        res = bool(AdminUser.query.filter_by(id = 1).first())
    except Exception as e:
        print(e)
        res = False
    if res:
        print('检测到已存在数据库')
        pass
    else:
        try:
            new_table()
            print('新数据库初始化完成')   
        except Exception as e:
            print(e)
            print('初始化失败,请检查数据库设置、防火墙、以及是否初始化完成')
    # try:
    #     if bool(AdminUser.query.filter_by(id = 1).first()):
    #         print('检测到已存在数据库')
    #         pass
    #     else:
    #         new_table()
    #         print('新数据库初始化完成')    
    # except:
    #     print('初始化失败,请检查数据库设置、防火墙、以及是否初始化完成')

init()


