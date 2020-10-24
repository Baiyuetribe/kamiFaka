from flask import Blueprint, Response,request,jsonify
from flask import render_template

import time

common = Blueprint('common', __name__,)


def Response_headers(content):  
    resp = Response(content)  
    resp.headers['Access-Control-Allow-Origin'] = '*'  
    return resp  


#前端
@common.route('/')
def index():
    return '恭喜，后端部署成功'
    # return render_template('index.html',title='flask & vue')


@common.route('/notify',methods=['POST','GET'])    #支付回调测试
def notify():
    print(request.form.to_dict()) #适用于post请求，但是回调时get请求
    content = str(request.form.to_dict())
    print(Response_headers(content))
    with open('note.log','a',encoding='utf=8') as f:
        f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' ' + str(Response_headers(content)))
    return Response_headers(content)

@common.route('/return',methods=['POST','GET'])    #支付回调测试
def back():
    print(request.json)
    with open('return.log','a',encoding='utf=8') as f:
        f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' ' + str(request.json))
    return jsonify(request.json)


@common.route('/robots.txt')
def robots():
    return Response('User-agent: *\n' + 'Disallow: /', 200, headers={'Content-Type': 'text/plain'})