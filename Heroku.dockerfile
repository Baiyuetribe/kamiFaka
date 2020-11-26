FROM python:3.8-slim
LABEL 维护者="佰阅 2894049053@qq.com"

# 备选数据库Sqlite \Mysql \ PostgreSQL
ENV DB_TYPE='PostgreSQL'

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN sed -i 's|postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE}|$DATABASE_URL|g' docker-entrypoint.sh && \
    sed -i 's|8000|$PORT|g' docker-entrypoint.sh && \
    chmod +x docker-entrypoint.sh

EXPOSE $PORT

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
