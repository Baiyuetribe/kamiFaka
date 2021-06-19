FROM baiyuetribe/kamifaka:latest
LABEL 维护者="佰阅 2894049053@qq.com"

# 备选数据库Sqlite \Mysql \ PostgreSQL
ENV DB_TYPE='PostgreSQL-Heroku'

WORKDIR /usr/src/app
RUN sed -i "s|'sqlite:///'+os.path.join(SQL_PATH,'kamifaka.db')|'${DATABASE_URL/'postgres'/'postgresql+psycopg2'}'|g" /usr/src/app/service/api/db.py && \
    sed -i '$d' docker-entrypoint.sh && \
    echo "gunicorn -k gevent --bind 0.0.0.0:${PORT} --workers 4 app:app" >> docker-entrypoint.sh && \
    # echo "gunicorn -k gevent --bind 0.0.0.0:8000 --workers 4 app:app" >> docker-entrypoint.sh && \
    # sed -i 's|8000|$PORT|g' docker-entrypoint.sh && \
    chmod +x docker-entrypoint.sh

EXPOSE $PORT

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
