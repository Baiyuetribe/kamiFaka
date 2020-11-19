FROM python:3.8-slim
LABEL 维护者="佰阅 2894049053@qq.com"

# 备选数据库Sqlite \Mysql
ENV DATABASE_TYPE='Mysql'

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN sed -i 's#mysql:\\/\\/${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}\\/${MYSQL_DATABASE}#$JAWSDB_URL#g' docker-entrypoint.sh && \
    sed -i 's/8000/$PORT/g' docker-entrypoint.sh && \
    chmod +x docker-entrypoint.sh

EXPOSE $PORT

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
