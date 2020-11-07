#!/bin/sh
echo '====^_^===='
echo '欢迎使用佰阅发卡(KAMIFAKA)程序'


if [ ${DATABASE_TYPE} = 'Mysql' ];then
sed -i "s/'sqlite:\/\/\/'+os.path.join(SQL_PATH,'kamifaka.db')/'mysql+pymysql:\/\/${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}\/${MYSQL_DATABASE}\?charset=utf8mb4'/g" /usr/src/app/service/api/db.py
fi

# 处理文件夹
if [ ! -d '/usr/src/app/public/images' ]; then
   mkdir /usr/src/app/public/images
fi
if [ ! -d '/usr/src/app/public/sql' ]; then
   mkdir /usr/src/app/public/images
fi
if [ ! -d '/usr/src/app/public/backups' ]; then
   mkdir /usr/src/app/public/backups
fi
if [ ! -e '/usr/src/app/public/images/null.png' ]; then
    cp -a /usr/src/app/service/system/* /usr/src/app/public/images/
fi

# 然后初始化数据库
python init_mysql.py

echo '程序初始化完成'
# ["gunicorn","-k", "gevent", "--bind", "0.0.0.0:8000", "--workers", "8", "app:app"]
gunicorn -k gevent --bind 0.0.0.0:8000 --workers 8 app:app