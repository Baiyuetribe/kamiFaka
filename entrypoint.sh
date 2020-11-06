#!/bin/sh

# Mysql数据库准备
mysql_ready() {
python << END
import sys
import MySQLdb
try:
    MySQLdb._mysql.connect(
        db="${MYSQL_DATABASE}",
        user="${MYSQL_USER}",
        passwd="${MYSQL_PASSWORD}",
        host="${MYSQL_HOST}",
        port=${MYSQL_PORT},
    )
except MySQLdb._exceptions.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

echo '数据库类型为：'${DATABASE_TYPE}

if [ "${DATABASE_TYPE}" = "Mysql" ];then
echo '数据库为Mysql，正在初始化操作'
#完成数据库替换
sed -i "s/os.path.join(SQL_PATH,\'kamifaka.db\')/\'${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}/${MYSQL_DATABASE}:${MYSQL_PORT}/?charset=utf8mb4\'/g" /usr/src/app/service/api/db.py
# 检测数据库是否初始化完成

export USERS_DATABASE_URI="mysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}"
until mysql_ready; do
>&2 echo 'Waiting for MySQL to become available...'
sleep 1
done
>&2 echo 'MySQL is available!'

# 开始执行其他任务
exec "$@"
fi

# 初始化数据库
python db_init.py
echo '数据库初始化完成，正在启动服务。。。'




# export USERS_DATABASE_URI="mysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}"

# mysql_ready() {
# python << END
# import sys
# import MySQLdb
# try:
#     MySQLdb._mysql.connect(
#         db="${MYSQL_DATABASE}",
#         user="${MYSQL_USER}",
#         passwd="${MYSQL_PASSWORD}",
#         host="${MYSQL_HOST}",
#         port=${MYSQL_PORT},
#     )
# except MySQLdb._exceptions.OperationalError as e:
#     print(e)
#     sys.exit(-1)
# sys.exit(0)
# END
# }
# until mysql_ready; do
#   >&2 echo 'Waiting for MySQL to become available...'
#   sleep 1
# done
# >&2 echo 'MySQL is available'

# exec "$@"
# echo "Waiting for MySQL..."


#     while ! nc -z db 3306; do
#     sleep 0.5
#     done

# echo "MySQL started"

