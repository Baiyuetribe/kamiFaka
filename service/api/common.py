from flask import Blueprint, Response,request,jsonify
from flask import render_template,redirect,send_from_directory
import time
import os

from flask.helpers import make_response

common = Blueprint('common', __name__)

def Response_headers(content):  
    resp = Response(content)  
    resp.headers['Access-Control-Allow-Origin'] = '*'  
    return resp  

import time
from functools import wraps

def timefn(fn):
    """计算性能的修饰器"""
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {t2 - t1: .5f} s")
        return result
    return measure_time

@common.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(common.root_path, '../../dist'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 图片公共路径
UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'../../public/images')



@common.route('/images/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_PATH,filename)



#前端
@common.route('/')
def index():
    # return '恭喜，后端部署成功'
    return render_template('index.html')
    # return """<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor: 
    # pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family: 
    # "Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal; 
    # margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"><p> 
    #  <br/><span style="font-size:30px">恭喜您,后端正常运行。</span></p></div> """   
#管理员---当前访客与管理员共用一套系统；后期可尝试分割管理员部分，更小的缩减前端体积
@common.route('/admin')
def admin():
    # return '恭喜，后端部署成功'
    return redirect('/#/admin')

@common.route('/login')
def login():
    return redirect('/#/admin')

# @common.route('/notify',methods=['POST','GET'])    #支付回调测试
# def notify():
#     print(request.form.to_dict()) #适用于post请求，但是回调时get请求
#     content = str(request.form.to_dict())
#     print(Response_headers(content))
#     with open('note.log','a',encoding='utf=8') as f:
#         f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' ' + str(Response_headers(content)))
#     return Response_headers(content)

# @common.route('/return',methods=['POST','GET'])    #支付回调测试
# def back():
#     print(request.json)
#     with open('return.log','a',encoding='utf=8') as f:
#         f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' ' + str(request.json))
#     return jsonify(request.json)

# @common.route('/demo')
# def demo():
#     content = 'xxxxxxxxxxxx'
#     res = make_response(content)
#     res.headers["Content-Disposition"] = "p_w_upload; filename=myfilename.txt"
#     return res


@common.route('/robots.txt')
def robots():
    return Response('User-agent: *\n' + 'Disallow: /images/', 200, headers={'Content-Type': 'text/plain'})
