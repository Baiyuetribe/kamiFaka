FROM python:3.8-slim
LABEL 维护者="佰阅 2894049053@qq.com"

# 备选数据库Sqlite \Mysql
ENV DATABASE_TYPE='Sqlite'
ENV MYSQL_HOST='127.0.0.1'  
ENV MYSQL_PORT='3306'  
ENV MYSQL_USER='KAMIFKA'  
ENV MYSQL_PASSWORD='PASSWORD'  
ENV MYSQL_DATABASE='KAMIFKA'  

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]

# ENTRYPOINT ["gunicorn","-k", "gevent", "--bind", "0.0.0.0:8000", "--workers", "8", "app:app"]


