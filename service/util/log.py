import time
# 定义日志记录器

# import sys

# def get_cur_info():
#     return sys._getframe().f_code.co_filename + ' 第' + str(sys._getframe().f_lineno)+'行'
# 获取具体路径位置 
# get_cur_info()


def log(msg):
    with open('service.log','a',encoding='utf=8') as f:
        f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' '+ str(msg))