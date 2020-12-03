import requests
import hashlib
import json
import re


class Epay:
    def __init__(self):
        from service.util.pay.pay_config import get_config    
        config = get_config('易支付')
        self.API = config['API']
        self.ID = config['ID']
        self.KEY = config['KEY']
        self.JUMP_URL = 'you_return_url'


    def create_order(self,name, out_trade_no, total_fee):
        data = {'notify_url': self.JUMP_URL, 'pid': self.ID, 'return_url': self.JUMP_URL, 'sitename': 'KAMIFAKA'}
        data.update(money=total_fee, name=name, out_trade_no=out_trade_no)
        items = data.items()
        items = sorted(items)
        wait_sign_str = ''
        for i in items:
            wait_sign_str += str(i[0]) + '=' + str(i[1]) + '&'
        wait_for_sign_str = wait_sign_str[:-1] + self.KEY
        # print("输出待加密字符串" + '\n' + wait_sign_str)
        sign = hashlib.md5(wait_for_sign_str.encode('utf-8')).hexdigest()
        data.update(sign=sign, sign_type='MD5')
        # print(data)
        try:
            req = requests.post(self.API + 'submit.php', data=data)
            # print(req.text)
            content = re.search(r"<script>(.*)</script>", req.text).group(1)
            # print(content)
            if 'http' in content:
                pay_url = re.search(r"href=\'(.*)\'", content).group(1)
            else:
                pay_url = self.API + re.search(r"\.?\/(.*)\'", content).group(1)
            return pay_url
        except Exception as e:
            # print('submit | API请求失败')
            print(e)
            return None


    def check(self,out_trade_no):
        try:
            req = requests.get(self.API + 'api.php?act=order&pid={}&key={}&out_trade_no={}'.format(self.ID, self.KEY, out_trade_no),
                            timeout=4)
    #         print(req.text)
            rst = re.search(r"(\{.*?\})", req.text).group(1)
            rst_dict = json.loads(rst)
            # print(rst_dict)
            code = str(rst_dict['code'])
            if int(code) == 1:
                pay_status = str(rst_dict['status'])
                if pay_status == '1':
                    # print('支付成功')
                    return True
            return None
        
        except Exception as e:
            print(e)
            # print('epay | 查询请求失败')
            return None


