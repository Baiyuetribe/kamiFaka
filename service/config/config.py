from service.database.models import *
from service.api.db import db

# 经验：先用true或false
def init_db(update=False):
    # 管理员信息
    db.session.add(AdminUser('admin@qq.com','$2b$12$BKSXKYuCgeXjr8IEbK02re0VhkFoAz7f3aHF3kYAMLzYaEiObqPYm'))
    # 邮箱配置
    # db.session.add(Smtp('demo@qq.com','卡密发卡网','smtp.qq.com','465','xxxxxxxxx',True))
    # 支付渠道
    db.session.add(Payment('支付宝当面付','支付宝',"{'APPID':'2016091800537528','alipay_public_key':'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4AHTfGleo8WI3qb+mSWOjJRyn6Vh8XvO6YsQmJjPnNKhvACHTHcU+PCUWUKZ54fSVhMkFZEQWMtAGeOt3lGy3pMBS96anh841gxJc2NUljU14ESXnDn4QdVe4bosmYvfko46wfA0fGClHdpO8UUiJGLj1W5alv10CwiCrYRDtx93SLIuQgwJn4yBC1/kE/KENOaWaA45dXIQvKh2P0lTbm0AvwYMVvYB+eB1GtOGQbuFJXUxWaMa0byTo9wSllhgyiIkOH+HJ9oOZIweGlsrezeUUdr3EEX97k25LdnUt/oQK8FIfthexfWZpTDDlHqmI7p6gCtRVDJenU4sxwpEyQIDAQAB','app_private_key':'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCqWmxsyPLwRmZHwoLYlUJXMF7PATKtvp7BrJfwLbxwrz6I48G11HpPPyAoNynwAMG7DCXjVX76NCbmfvvPqnbk09rNRULqGju8G6NkQTbLfDjhJs+CE8kdIs89btxqDG70ebePiZTGpQngPLfrziKDOhRfXkA5qRPImbC+PUXiXq9qvkp9Yu/8IYjyxUpNBNjZuTK+fTjSI0RCt7eE+wR0KqpNIzot1q/ds1KTIYmJQM5tEFie4BK0pDtGiIs/VrUG8PTPqLyzEyIMy1N75olUWAiGrk0USqiieP3TYj0PdlQDX2T14DOwMkl5Rjvt7Knc+WGdolPIBssUX1wTE+J7AgMBAAECggEAWpRP+Jv0yRu1wMxFRKJArxmSH+GUL9wej/6Un2nCO+yChMkNtAAxtLdtAtUqIGpWmH2CG9nW9XULhh3ZCPer1kprmiAMz2t5fbD4dRNT7miz2cwIJDMfCbX7mb+7xUutJ6Mcnl7aU7FnierfJKvrn/ke4gK8haxIT66g0tbDtPQhYnGPawyM+gqFulaMBcuqH0naAIq5ZBWHkKuuwJ1SD6yGrWgHdq3Kt2pE8b9yjfdUl15IeW0rszXG6fTika9WX6qaulyoGAAZdjiXED+mbRyqZA3jq7RI38qBP9+/jAb+fdwE8EwqnpPvfGHMBdkREOXK0kzRU8rpd9GbH7INaQKBgQDwpuW+bK/qxKx3BSAXL98f0J2I7YVuk0EFCStGoxnzWRv0yvL0QEDwN+QPiVMmcVQcr79mW5zTBkd4vmr3ud+v1f/X6UPI82kQhZlVWry8LEnisPlZuE0E/EaJrLgF7z4l3ItzCVi8IfpgizPcCYSz/vY49a5W34eKjXHWUB1jDwKBgQC1N8PgGKI2LRDaJeqt5Ef6yyYSMOgVe0WSqAlgyMECb1pjmMBjcNG1AFE/FfgNu4thOaXIogElGVoQFvA5GuJQY48HOJNgx3Ua2SxiowcXkAN0gIm4FY+ozkp7xhizvLVfsmX+MKqPtl6nggiWETJJyvMQnjMgKLmSvhsopMwZ1QKBgGV36az2BOK3VITGq3Y7YBf5DUN76uPpwOOPryiUgs+hhfEcVX55TSg8WLPYUjAGXtHNpKVTAXfU0PPvTgjv3Yo1cC+okkU7pNQrkLB1lti8z9Z+ilSzKf5tJIzOP7V437p1GHNDwJ9qsDhe2VnwxXxjh4wSwxSsIWlhJFuZ4hovAoGAFgm8Fmqof3InlH/79D3IyyUdciTkdIhTQ6yPx2dioYstMOOIsg8sUZjCSKvBSNo/7wj1slqRTROyMja37Bnq39/bqwMkWSaohSVYEn7FBAaNhQOEvBBTMjI0OK00n9cZL5QgdzMv6t5A0JottSJOPU8jFChJC2Yoe0IHR4ATGikCgYB2smi7/ptKiGdwmiuUHsF/U3jfjpHyHwLrXjoSU+mwV+GjqcdbtkSP1suGjN8tcdbFvLSCRX/IRdFHYJeuPUXQtZtiC431+upasbEiJ1xZ2KcK3lKf0mOn10kPD5QC7mmsfmjz4cw9cSrBjmcWGXeIwIXPLhOAAIzpHqy8oP/F/g=='}",'alipay.com 官方接口0.38~0.6%',True))
    db.session.add(Payment('微信官方接口','微信支付',"{'APPID':'XXXXXXXX','MCH_ID':'XXXXXX','APP_SECRET':'XXXXXX'}",'pay.weixin.qq.com 微信官方0.38%需要营业执照',False))
    db.session.add(Payment('虎皮椒支付宝','支付宝',"{'API':'api.vrmrgame.com','appid':'XXXXXX','AppSecret':'YYYYY'}",'xunhupay.com 个人接口0.38%+1~2%',False))
    db.session.add(Payment('虎皮椒微信','微信支付',"{'API':'api.vrmrgame.com','appid':'XXXXXX','AppSecret':'YYYYY'}",'xunhupay.com 个人接口0.38~0.6%+1~2%',False))
    db.session.add(Payment('PAYJS支付宝','支付宝',"{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}",'payjs.cn 个人接口2.38%',False))
    db.session.add(Payment('PAYJS微信','微信支付',"{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}",'payjs.cn 个人接口2.38%',False))
    db.session.add(Payment('码支付支付宝','支付宝',"{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}",'codepay.fateqq.com挂机宝 不可用',False))
    db.session.add(Payment('码支付微信','微信支付',"{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}",'codepay.fateqq.com挂机宝 不可用',False))
    db.session.add(Payment('码支付QQ','QQ支付',"{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}",'codepay.fateqq.com挂机宝 不可用',False))
    db.session.add(Payment('易支付','易支付',"{'API':'http://google.com','ID':'XXXXX','KEY':'YYYYYYYY'}",'支持订单查询接口的任意易支付 高费率不稳定',False))
    db.session.add(Payment('Mugglepay','Mugglepay',"{'TOKEN':'xxxxxx','Currency':'CNY','Web_url':'https://google.com'}",'mugglepay.com全球综合收款系统 高费率',False))
    db.session.add(Payment('YunGouOS','微信或支付宝支付',"{'mch_id':'xxxxxx','pay_secret':'yyyyyyy'}",'yungouos.com 微信或支付宝个体0.38%',False))
    db.session.add(Payment('YunGouOS_WXPAY','微信支付',"{'mch_id':'xxxxxx','pay_secret':'yyyyyyy'}",'yungouos.com 微信个体0.38%',False))

    # 商品分类
    db.session.add(ProdCag('账户ID','虚拟账号类商品','100'))
    db.session.add(ProdCag('激活码','单独激活类商品','1000'))
    db.session.add(ProdCag('第三分类','单独激活类商品','1000'))
    # 商品设置
    db.session.add(ProdInfo('账户ID','普通商品演示','商品简述信息演示XXXX','images/null.png','100','演示：我是商品描述信息',\
                                9.99,None, True,0,0,True))
    db.session.add(ProdInfo('账户ID','批发商品演示','商品简述信息演示XXXX','images/null.png','100','演示：我是商品描述信息',\
                                9.99,'9#9.9,8.8', True,0,0,True))
    db.session.add(ProdInfo('账户ID','普通商品DD','商品简述信息演示XXXX','images/null.png','100','演示：我是商品描述信息',\
                                9.99,None, False,0,0,False))                                
    db.session.add(ProdInfo('激活码','重复卡密演示','商品简述信息演示XXXX','images/null.png','100','演示：我是商品描述信息',\
                                9.99,None, True,0,0,True))
    db.session.add(ProdInfo('激活码','普通商品CC','商品简述信息演示XXXX','images/null.png','100','演示：我是商品描述信息',\
                                9.99,None, True,0,0,True))
    db.session.add(ProdInfo('激活码','普通商品BB','商品简述信息演示XXXX','images/null.png','100','演示：我是商品描述信息',\
                                9.99,None,True,0,0,False))        
    # 卡密设置
    db.session.add(Card('普通商品演示','454545454454545454',False,False))
    db.session.add(Card('批发商品演示','555555555555555555',False,False))
    db.session.add(Card('批发商品演示','666666666666666666',False,False))
    db.session.add(Card('重复卡密演示','666666666666666666',True,False))
    # 系统配置
    db.session.add(Config('web_name','KAMIFAKA','网站名称',True))
    db.session.add(Config('web_keyword','关键词、收录词汇','网站关键词',True))
    db.session.add(Config('description','网站描述信息。。。','网站描述',True))
    db.session.add(Config('web_url','【预留不填】','网站地址，同步回调时调用',True))
    db.session.add(Config('web_bg_url','https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/colorfull.jpg','网站背景图片',True))
    db.session.add(Config('contact_us','<p>示例，请在管理后台>>网站设置里修改，支持HTML格式</p>','首页-联系我们',True))
    # db.session.add(Config('web_footer','【未开发】','可填写备案信息',True))
    db.session.add(Config('top_notice','首页公告栏信息,请在管理后台,网站设置里修改，支持HTML格式','首页公告',True))
    # db.session.add(Config('modal_notice','【计划中】','全局弹窗信息',True))
    db.session.add(Config('toast_notice','演示站随时更新，可优先体验新功能','首页滑动消息设置',True))
    db.session.add(Config('theme','list','主题',False))
    db.session.add(Config('kamiFaka','https://github.com/Baiyuetribe/kamiFaka','Github项目地址，用于手动检测新版',False))
    db.session.add(Config('kamiFaka_v','1.6','Github项目地址，用于手动检测新版',False))

    # 通知渠道 ：名称；对管理员开关；对用户开关；对管理员需要管理员账号；用户无；名称+config+管理员+admin_switch+user_switch
    db.session.add(Notice('邮箱通知',"{'sendname':'no_replay','sendmail':'demo@gmail.com','smtp_address':'smtp.qq.com','smtp_port':'465','smtp_pwd':'ZZZZZZZ'}",'demo@qq.com',False,False))
    db.session.add(Notice('微信通知',"{'token':'AT_nvlYDjev89gV96hBAvUX5HR3idWQwLlA'}",'xxxxxxxxxxxxxxxx',False,False))
    db.session.add(Notice('TG通知',"{'TG_TOKEN':'1290570937:AAHaXA2uOvDoGKbGeY4xVIi5kR7K55saXhs'}",'445545444',False,False))
    db.session.add(Notice('短信通知',"{'username':'XXXXXX','password':'YYYYY','tokenYZM':'必填','templateid':'必填'}",'15347875415',False,False))
    db.session.add(Notice('QQ通知',"{'Key':'null'}",'格式：您的KEY@已添加的QQ号,示例：abc@123',False,False))

    # 订单信息【测试环境】
    db.session.add(Order('演示订单4454','普通商品演示','支付宝当面付','472835979','请求尽快发货',9.99,1,0.9,'账号：xxxxx；密码：xxxx',None,None))
    db.session.add(Order('演示订单4455','普通商品演示','虎皮椒微信','458721@qq.com','非常感谢',9.99,3,1.97,None,None,None))    #卡密为None或‘’空都可以
    db.session.add(Order('Order_1608107857954q7kyldyg','普通商品演示','虎皮椒支付宝','demo@gmail.com','不错',9.99,1,0.9,'此处为卡密',None,None))
    db.session.add(Order('演示订单4457','普通商品演示','虎皮椒支付宝','472835979','不错',9.99,1,1.9,'TG卡密DEMO',None,None))
    
    # 插件配置信息
    db.session.add(Plugin('TG发卡',"{'TG_TOKEN':'1488086653:AAHihuO0JuvmiDNZtsYcDBpUhL1rTDO6o1C'}",'### 示例 \n请在管理后台--》Telegram里设置，支持HTML格式',False)) 
    db.session.add(Plugin('微信公众号',"{'PID':'xxxxxxxxxxxx'}",'<p>示例，请在管理后台>>Telegram里设置，支持HTML格式</p>',False)) 

    db.session.commit()

