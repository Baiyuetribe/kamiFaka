import time
# 定义日志记录器

def log(msg):
    with open('service.log','a',encoding='utf=8') as f:
        f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' ' + str(msg))