"""
短信接口集成：
由于国内绝大部分接口都需要营业执照才能发自定义消息，因此已放弃阿里云、腾讯云等短信接口。
"""
#文字短信DEMO
import urllib.request
import urllib
import json
import hashlib
import time

#参数配置

def sms_txt(config,param):
    base_url = "http://www.lokapi.cn/smsUTF8.aspx"
    rece = "json"
    username = config['username']
    password = config['password']
    #验证码
    tokenYZM = config['tokenYZM']
    templateid = config['templateid'] 
    #参数
    param = param


    def MD5(str):
        m = hashlib.md5()
        m.update(str.encode(encoding='UTF-8'))
        return m.hexdigest().upper()

    #密码加密
    passwd = MD5(password)

    #时间戳
    ticks =int(time.time() * 1000)

    #构造发送主体
    dict = {"action": "sendtemplate", "username": username,
            "password": passwd, "token": tokenYZM, "timestamp": ticks}
    body = "action=sendtemplate&username={username}&password={password}&token={token}&timestamp={timestamp}".format(username=username,password=passwd,token=tokenYZM,timestamp=ticks
    )
    sign = MD5(body)
    dict["sign"] = sign
    dict["rece"] = rece
    dict["templateid"] = templateid
    dict["param"] = param

    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
    data = urllib.parse.urlencode(dict).encode('utf-8')
    request = urllib.request.Request(base_url, data, headers)
    text_rece = urllib.request.urlopen(request).read().decode('utf-8')
    print("文字短信接收数据："+ text_rece)

    '''
    您购买的XXXX卡密内容为：YYYYYY
    '''


def sms_to_user(config,data):
    # print(config)
    # print(data)
    card = data['card'][:50]
    param = data['contact']+'|'+card
    # param='XXXXXXX|DEMO测试消息'
    sms_txt(config,param)

    pass


def sms_to_admin(config,admin_account,data):
    # print(config)
    # print(admin_account)
    param = str(admin_account)+'|'+data['contact']+'下单成功'
    sms_txt(config,param)
    # print(f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！")

def sms_test(config,message,mobile):
    # print(config)
    # print(admin_account)
    param = str(mobile)+'|'+str(message)
    sms_txt(config,param)
    # print(f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！")