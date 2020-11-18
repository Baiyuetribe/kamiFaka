from email import message
import requests
from service.database.models import Notice

def wxpush(config,admin_account,data):
    # 传入参数
    # 要求
    # 设置推送信息
    if data['contact_txt']:
        content = f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！备注信息：{data['contact_txt']}",
    else:
        content = f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！",    
    data = {
        'appToken':config['token'],
        'content':content,
        # 'summary':'发卡网消息提示',
        'contentType':1,    #内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown 
        'uids':[f"{admin_account}"]
    }
    requests.post('http://wxpusher.zjiecode.com/api/send/message',json=data)
    # print(r)
    # print(r.json())
