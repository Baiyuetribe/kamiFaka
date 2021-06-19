FROM baiyuetribe/kamifaka:latest
LABEL 维护者="佰阅 2894049053@qq.com"

ENV DB_TYPE='PostgreSQL-Heroku'

RUN sed -i "s|'# 处理文件夹'|'sed -i \"s\|'sqlite:///'+os.path.join(SQL_PATH,'kamifaka.db')\|'\${DATABASE_URL/'postgres'/'postgresql+psycopg2'}'\|g\" /usr/src/app/service/api/db.py'|g" docker-entrypoint.sh & \
    sed -i '$d' docker-entrypoint.sh && \
    echo "gunicorn -k gevent --bind 0.0.0.0:\${PORT} --workers 4 app:app" >> docker-entrypoint.sh

EXPOSE $PORT

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
