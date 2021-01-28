import requests

def qqpush(config,admin_account,data):
    # 传入参数
    # 要求
    # 设置推送信息
    if data['contact_txt']:
        content = f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！备注信息：{data['contact_txt']}"
    else:
        content = f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！"
    try:
        key,qq = admin_account.split('@')
        data = {
            'msg':content,
            'qq':qq
        }
        requests.post('https://qmsg.zendee.cn/send/'+key,data=data)        
    except:
        print('没有正确的填写格式')
        return None
