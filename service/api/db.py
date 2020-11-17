from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# from requests.api import options
import datetime
import os
# from flask_socketio import SocketIO
#通用组件
app = Flask(__name__,static_folder='../../dist/static',template_folder='../../dist')
# app = Flask(__name__,static_folder='../../dist',template_folder='../../dist')
# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

# #避免与vue冲突
# app.jinja_env.variable_start_string = '{['
# app.jinja_env.variable_end_string = ']}'

# socketio = SocketIO(app, cors_allowed_origins='*')

#路径设置
SQL_PATH = os.path.join(os.path.dirname(__file__),'../../public/sql')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'   #本地
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///'+os.path.join(SQL_PATH,'kamifaka.db')   #默认数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:336/KAFAKA?charset=utf8mb4'   #本地
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kmfaka:iY5r57Cc34a8LSk7@47.105.152.9:3306/kmfaka?charset=utf8mb4'   #远程
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://docker_db_1:root@127.0.0.1:3306/KAFAKA?charset=utf8mb4'   #本地

# mysql mysql+pymysql://root:wujing0126@127.0.0.1:3306/gbs?charset=utf8
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension. Read more: https://flask-jwt-extended.readthedocs.io/en/stable/options/
app.config['JWT_SECRET_KEY'] = 'a44545de51d5e4deaswdedcecvrcrfr5f454fd1cec415r4f'  # Change this!
app.config['JWT_ACCESS_TOKEN EXPIRES'] = datetime.timedelta(days=2)
jwt = JWTManager(app)

# 解决与vue3模板冲突
# app.jinja_env.variable_start_string = '[['
# app.jinja_env.variable_end_string = ']]'

# options = {
#     'variable_start_string':'(%',
#     'variable_end_string':'%)',
# }
# app.jinja_options.update(options)
# CORS(app, supports_credentials=True)    #解决跨域问题

db = SQLAlchemy(app)

