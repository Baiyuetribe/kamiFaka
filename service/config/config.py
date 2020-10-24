from service.database.models import AdminUser,Config,Payment,ProdCag,ProdInfo,Order,Card,Notice,Message
from service.api.db import db

# 经验：先用true或false
def init_db(update=False):
    # db.session.add(User('admin','123456'))
    # 管理员信息
    db.session.add(AdminUser('admin@qq.com','$2b$12$BKSXKYuCgeXjr8IEbK02re0VhkFoAz7f3aHF3kYAMLzYaEiObqPYm'))
    # 邮箱配置
    # db.session.add(Smtp('demo@qq.com','卡密发卡网','smtp.qq.com','465','xxxxxxxxx',True))
    # 支付渠道
    db.session.add(Payment('支付宝当面付','./aipay.png',"{'APPID':'2016091800537528','alipay_public_key':'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4AHTfGleo8WI3qb+mSWOjJRyn6Vh8XvO6YsQmJjPnNKhvACHTHcU+PCUWUKZ54fSVhMkFZEQWMtAGeOt3lGy3pMBS96anh841gxJc2NUljU14ESXnDn4QdVe4bosmYvfko46wfA0fGClHdpO8UUiJGLj1W5alv10CwiCrYRDtx93SLIuQgwJn4yBC1/kE/KENOaWaA45dXIQvKh2P0lTbm0AvwYMVvYB+eB1GtOGQbuFJXUxWaMa0byTo9wSllhgyiIkOH+HJ9oOZIweGlsrezeUUdr3EEX97k25LdnUt/oQK8FIfthexfWZpTDDlHqmI7p6gCtRVDJenU4sxwpEyQIDAQAB','app_private_key':'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCqWmxsyPLwRmZHwoLYlUJXMF7PATKtvp7BrJfwLbxwrz6I48G11HpPPyAoNynwAMG7DCXjVX76NCbmfvvPqnbk09rNRULqGju8G6NkQTbLfDjhJs+CE8kdIs89btxqDG70ebePiZTGpQngPLfrziKDOhRfXkA5qRPImbC+PUXiXq9qvkp9Yu/8IYjyxUpNBNjZuTK+fTjSI0RCt7eE+wR0KqpNIzot1q/ds1KTIYmJQM5tEFie4BK0pDtGiIs/VrUG8PTPqLyzEyIMy1N75olUWAiGrk0USqiieP3TYj0PdlQDX2T14DOwMkl5Rjvt7Knc+WGdolPIBssUX1wTE+J7AgMBAAECggEAWpRP+Jv0yRu1wMxFRKJArxmSH+GUL9wej/6Un2nCO+yChMkNtAAxtLdtAtUqIGpWmH2CG9nW9XULhh3ZCPer1kprmiAMz2t5fbD4dRNT7miz2cwIJDMfCbX7mb+7xUutJ6Mcnl7aU7FnierfJKvrn/ke4gK8haxIT66g0tbDtPQhYnGPawyM+gqFulaMBcuqH0naAIq5ZBWHkKuuwJ1SD6yGrWgHdq3Kt2pE8b9yjfdUl15IeW0rszXG6fTika9WX6qaulyoGAAZdjiXED+mbRyqZA3jq7RI38qBP9+/jAb+fdwE8EwqnpPvfGHMBdkREOXK0kzRU8rpd9GbH7INaQKBgQDwpuW+bK/qxKx3BSAXL98f0J2I7YVuk0EFCStGoxnzWRv0yvL0QEDwN+QPiVMmcVQcr79mW5zTBkd4vmr3ud+v1f/X6UPI82kQhZlVWry8LEnisPlZuE0E/EaJrLgF7z4l3ItzCVi8IfpgizPcCYSz/vY49a5W34eKjXHWUB1jDwKBgQC1N8PgGKI2LRDaJeqt5Ef6yyYSMOgVe0WSqAlgyMECb1pjmMBjcNG1AFE/FfgNu4thOaXIogElGVoQFvA5GuJQY48HOJNgx3Ua2SxiowcXkAN0gIm4FY+ozkp7xhizvLVfsmX+MKqPtl6nggiWETJJyvMQnjMgKLmSvhsopMwZ1QKBgGV36az2BOK3VITGq3Y7YBf5DUN76uPpwOOPryiUgs+hhfEcVX55TSg8WLPYUjAGXtHNpKVTAXfU0PPvTgjv3Yo1cC+okkU7pNQrkLB1lti8z9Z+ilSzKf5tJIzOP7V437p1GHNDwJ9qsDhe2VnwxXxjh4wSwxSsIWlhJFuZ4hovAoGAFgm8Fmqof3InlH/79D3IyyUdciTkdIhTQ6yPx2dioYstMOOIsg8sUZjCSKvBSNo/7wj1slqRTROyMja37Bnq39/bqwMkWSaohSVYEn7FBAaNhQOEvBBTMjI0OK00n9cZL5QgdzMv6t5A0JottSJOPU8jFChJC2Yoe0IHR4ATGikCgYB2smi7/ptKiGdwmiuUHsF/U3jfjpHyHwLrXjoSU+mwV+GjqcdbtkSP1suGjN8tcdbFvLSCRX/IRdFHYJeuPUXQtZtiC431+upasbEiJ1xZ2KcK3lKf0mOn10kPD5QC7mmsfmjz4cw9cSrBjmcWGXeIwIXPLhOAAIzpHqy8oP/F/g=='}",'官方接口 稳定可靠',True))
    db.session.add(Payment('虎皮椒支付宝','./aipay.png',"{'appid':'XXXXXX','AppSecret':'YYYYY'}",'官方合作接口 个人账户到账',True))
    db.session.add(Payment('虎皮椒微信','./aipay.png',"{'appid':'XXXXXX','AppSecret':'YYYYY'}",'官方合作接口 个人账户到账',True))
    db.session.add(Payment('PAYJS支付宝','./aipay.png',"{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}",'官方合作接口 个人账户到账',True))
    db.session.add(Payment('PAYJS微信','./aipay.png',"{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}",'官方合作接口 个人账户到账',True))
    db.session.add(Payment('码支付支付宝','./aipay.png',"{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}",'挂机宝 个人账户到账',True))
    db.session.add(Payment('码支付微信','./aipay.png',"{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}",'挂机宝 个人账户到账',True))
    db.session.add(Payment('码支付QQ','./aipay.png',"{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}",'挂机宝 个人账户到账',True))

    # 商品分类
    db.session.add(ProdCag('账户ID','虚拟账号类商品','100'))
    db.session.add(ProdCag('激活码','单独激活类商品','1000'))
    db.session.add(ProdCag('第三分类','单独激活类商品','1000'))
    # 商品设置
    db.session.add(ProdInfo('账户ID','香港ID','示例：适用于苹果IOS设备登录app store下载港区特有游戏或软件','./upload/images/451244.png','100','下单后获得港区账号密码，苹果手机端打开app store登录账号，即可下载港区软件，完成后注销并重新登录自己的账号，已安装的应用就就可以正常使用',\
                                9.99, True,0,0,True))
    db.session.add(ProdInfo('账户ID','香港ID2','示例：适用于苹果IOS设备登录app store下载港区特有游戏或软件','./upload/images/451244.png','100','下单后获得港区账号密码，苹果手机端打开app store登录账号，即可下载港区软件，完成后注销并重新登录自己的账号，已安装的应用就就可以正常使用',\
                                9.99, True,0,0,True))
    db.session.add(ProdInfo('账户ID','香港ID3','示例：适用于苹果IOS设备登录app store下载港区特有游戏或软件','./upload/images/451244.png','100','下单后获得港区账号密码，苹果手机端打开app store登录账号，即可下载港区软件，完成后注销并重新登录自己的账号，已安装的应用就就可以正常使用',\
                                9.99, False,0,0,False))                                
    db.session.add(ProdInfo('激活码','香港ID4','示例：适用于苹果IOS设备登录app store下载港区特有游戏或软件','./upload/images/451244.png','100','下单后获得港区账号密码，苹果手机端打开app store登录账号，即可下载港区软件，完成后注销并重新登录自己的账号，已安装的应用就就可以正常使用',\
                                9.99, False,0,0,False))
    db.session.add(ProdInfo('激活码','香港ID5','示例：适用于苹果IOS设备登录app store下载港区特有游戏或软件','./upload/images/451244.png','100','下单后获得港区账号密码，苹果手机端打开app store登录账号，即可下载港区软件，完成后注销并重新登录自己的账号，已安装的应用就就可以正常使用',\
                                9.99, True,0,0,True))
    db.session.add(ProdInfo('激活码','香港ID6','示例：适用于苹果IOS设备登录app store下载港区特有游戏或软件','./upload/images/451244.png','100','下单后获得港区账号密码，苹果手机端打开app store登录账号，即可下载港区软件，完成后注销并重新登录自己的账号，已安装的应用就就可以正常使用',\
                                9.99, True,0,0,False))        
    # 卡密设置
    db.session.add(Card('香港ID','454545454454545454',False,False))
    db.session.add(Card('香港ID','555555555555555555',True,False))
    db.session.add(Card('香港ID','666666666666666666',False,False))
    # 系统配置
    db.session.add(Config('web_name','KAMIFAKA','网站名称'))
    db.session.add(Config('web_keyword','关键词、收录词汇','网站关键词'))
    db.session.add(Config('web_url','https://baiyue.one','网站地址，支付回调时调用'))
    db.session.add(Config('web_bg_url','https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/colorfull.jpg','网站背景图片'))
    db.session.add(Config('web_logo','./logo.png','logo'))
    db.session.add(Config('web_footer','','可填写备案或统计信息'))
    db.session.add(Config('top_notice','首页公告栏信息','首页公告'))
    db.session.add(Config('modal_notice','','全局弹窗信息'))
    db.session.add(Config('toast_notice','欢迎访问本站！','加载后欢迎也消息'))
    db.session.add(Config('login_captcha','false','登录验证码'))
    db.session.add(Config('search_captcha','false','查询订单验证码'))
    db.session.add(Config('theme','list_theme','主题'))
    db.session.add(Config('kamiFaka','https://github.com/Baiyuetribe/kamiFaka','Github项目地址，用于手动检测新版'))
    db.session.add(Config('kamiFaka_v','1.0.0','Github项目地址，用于手动检测新版'))


    # 通知栏
    # db.session.add(Message(True,'示例：顶部消息栏通知','顶部公告'))
    # db.session.add(Message(False,'示例：弹窗消息','全局弹窗公告'))

    # 通知渠道 ：名称；对管理员开关；对用户开关；对管理员需要管理员账号；用户无；名称+config+管理员+admin_switch+user_switch
    db.session.add(Notice('邮箱通知',"{'sendname':'no_replay','sendmail':'demo@gmail.com','smtp_address':'smtp.qq.com','smtp_port':'465','smtp_pwd':'ZZZZZZZ'}",'demo@qq.com',False,False))
    db.session.add(Notice('微信通知',"{'token':'开发中'}",'xxxxxxxxxxxxxxxx',False,False))
    db.session.add(Notice('TG通知',"{'TG_TOKEN':'1290570937:AAHaXA2uOvDoGKbGeY4xVIi5kR7K55saXhs'}",'472835979',True,False))
    db.session.add(Notice('短信通知',"{'appid':'XXXXXX','AppSecret':'YYYYY'}",'15347875415',False,False))


    # 订单信息【测试环境】
    db.session.add(Order('baiyue4512454544','香港ID','支付宝当面付','1563254111','请求尽快发货',9.99,1,9.9,'账号：xxxxx；密码：xxxx'))
    db.session.add(Order('baiyue4512454546','香港ID','虎皮椒微信','458721@qq.com','非常感谢',9.99,3,29.97,None))    #卡密为None或‘’空都可以
    db.session.add(Order('baiyue4512454548','香港ID','虎皮椒支付宝','demo@gmail.com','不错',9.99,1,9.9,''))
    # 
    
    db.session.commit()

