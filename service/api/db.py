from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from requests.api import options

# from flask_socketio import SocketIO
#通用组件
app = Flask(__name__)
CORS(app)    #解决跨域问题
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

# socketio = SocketIO(app, cors_allowed_origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'   #本地
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:336/KAFAKA?charset=utf8mb4'   #本地
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://docker_db_1:root@127.0.0.1:3306/KAFAKA?charset=utf8mb4'   #本地

# mysql mysql+pymysql://root:wujing0126@127.0.0.1:3306/gbs?charset=utf8
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension. Read more: https://flask-jwt-extended.readthedocs.io/en/stable/options/
app.config['JWT_SECRET_KEY'] = 'a44545de51d5e4deaswdedcecvrcrfr5f454fd1cec415r4f'  # Change this!
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

