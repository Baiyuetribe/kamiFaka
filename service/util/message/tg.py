from os import name
from service.database.models import Notice
from requests import post

"""
TG 消息推送
"""

def post_tg(config,admin_account,data):
    #默认为文本消息
    TG_TOKEN = config['TG_TOKEN']
    CHAT_ID = admin_account   
    telegram_message = f"管理员您好：{data['contact']}购买的{data['name']}卡密发送成功！"
               
    params = (
        ('chat_id', CHAT_ID),
        ('text', telegram_message),
        ('parse_mode', "Markdown"), #可选Html或Markdown
        ('disable_web_page_preview', "yes")
    )    
    telegram_url = "https://api.telegram.org/bot" + TG_TOKEN + "/sendMessage"
    telegram_req = post(telegram_url, params=params)
    telegram_status = telegram_req.status_code
    # if telegram_status == 200:
    #     print(f"INFO: Telegram Message sent")
    # else:
    #     print("Telegram Error")
        
if __name__ == "__main__":
    post_tg('你好，佰阅！')    
    # t.me/kamiFaka_bot  公共频道