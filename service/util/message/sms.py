"""
短信接口集成：
由于国内绝大部分接口都需要营业执照才能发自定义消息，因此已放弃阿里云、腾讯云等短信接口。
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