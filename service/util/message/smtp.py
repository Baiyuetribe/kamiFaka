from email import message
from operator import sub
import smtplib
import email
from email.mime.text import MIMEText


class MailSender(object):
    def __init__(self, user: str, password: str, host: str, port: int):
        self.__user = user
        # 提取出邮箱地址用于登录
        self.__login_mail = email.utils.getaddresses([user])[0][1]
        # 连接到smtp服务器，限制只允许使用25、465、587这三个端口
        if port == 25:
            self.__smtp_server = smtplib.SMTP(host=host, port=port)
        elif port == 465:
            self.__smtp_server = smtplib.SMTP_SSL(host=host, port=port)
        elif port == 587:
            self.__smtp_server = smtplib.SMTP(host=host, port=port)
            self.__smtp_server.starttls()
        else:
            raise ValueError("Can only use port 25, 465 and 587")

        # 登录smtp服务器
        self.__smtp_server.login(user=self.__login_mail, password=password)

    def send(self, to_user: str, subject: str = "", content: str = "", subtype: str = "plain"):
        """
        发送纯文本邮件
        :param to_user: 收件人，支持 name<prefix@example.com> 的形式，如需同时发给多人，将多个收件人用半角逗号隔开即可
        :param subject: 邮件主题，默认为空字符串
        :param content: 邮件正文，默认为空字符串
        :param subtype: 邮件文本类型，只能为 plain 或 html，默认为 plain
        """
        self.__check_subtype(subtype)

        # 构造邮件
        msg = MIMEText(content, _subtype=subtype, _charset="utf-8")
        msg["From"] = self.__user
        msg["To"] = to_user
        msg["subject"] = subject

        # 发送邮件
        self.__smtp_server.send_message(msg)


    def __check_subtype(self, subtype: str):
        if subtype not in ("plain", "html"):
            raise ValueError('Error subtype, only "plain" and "html" can be used')
        else:
            pass


def mail_to_user(config,data):
    # 收件人、主题、数据（）
    mail = MailSender(user=config['sendmail'],password=config['smtp_pwd'],host=config['smtp_address'],port=int(config['smtp_port']))
    # data：对用户而言是prod_name,卡密信息+订单ID;；对管理员而言是contact购买prod_name成功！
    subject = '订单通知：'+data['name']
    # content = f"<h5>您好{data['contact']}! 您购买的{data['name']}商品，卡密信息是：{data['card']}<h5>"    #模板后期待完善
    try:
        from service.database.models import Config  #传递网站名称和url地址信息
        web_name = Config.query.filter_by(name = 'web_name').first().to_json()
        web_url = Config.query.filter_by(name = 'web_url').first().to_json()
        data['web_name'] = web_name['info']
        data['web_url'] = web_url['info']
        from service.util.message.card_theme import card
        content = card(data)    
        #定义邮件样式：
        mail.send(to_user=data['contact'],subject=subject,content=content,subtype='html')
        return True
    except:
        return False

def mail_to_admin(config,admin_account,data):
    # 收件人、主题、数据（）
    mail = MailSender(user=config['sendmail'],password=config['smtp_pwd'],host=config['smtp_address'],port=int(config['smtp_port']))
    # data：对用户而言是prod_name,卡密信息+订单ID;；对管理员而言是contact购买prod_name成功！
    subject = '管理员通知：'
    content = f"<h5>{data['contact']}购买的{data['name']}卡密发送成功！<h5>"    #模板后期完成
    #定义邮件样式：
    mail.send(to_user=admin_account,subject=subject,content=content,subtype='html')

def mail_test(config,message,email):
    try:
        mail = MailSender(user=config['sendmail'],password=config['smtp_pwd'],host=config['smtp_address'],port=int(config['smtp_port']))
        subject = '管理员邮件测试'
        content = message
        mail.send(to_user=email,subject=subject,content=content,subtype='html')
        return True
    except:
        return False
    

