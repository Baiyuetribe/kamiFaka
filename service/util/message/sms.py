"""
征集接口信息，可积极反馈，附上开发文档地址即可
"""

def sms_to_user(config,data):
    print(config)
    print(data)
    pass

def sms_to_admin(config,admin_account,data):
    print(config)
    print(admin_account)
    print(f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！")
    pass