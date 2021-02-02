FROM baiyuetribe/kamifaka:v1.6
LABEL 维护者="佰阅 2894049053@qq.com"

# 备选数据库Sqlite \Mysql \ PostgreSQL
ENV DB_TYPE='PostgreSQL'

WORKDIR /usr/src/app

RUN echo "<!DOCTYPE html><html lang='zh-cn'><head><meta charset='utf-8'><meta http-equiv='X-UA-Compatible' content='IE=edge'><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='icon' href='images/favicon.ico'><link href='https://cdn.jsdelivr.net/gh/Baiyuetribe/kamifaka@CDN/v1.6/static/css/vendor.0784d59c.css' rel='stylesheet'><link href='https://cdn.jsdelivr.net/gh/Baiyuetribe/kamifaka@CDN/v1.6/static/css/styles.7e54a98a.css' rel='stylesheet'></head><body><noscript><strong>We're sorry but kamifaka doesn't work properly without JavaScript enabled. Please enable it to            continue.</strong></noscript><div id='app'></div><script src='https://cdn.jsdelivr.net/gh/Baiyuetribe/kamifaka@CDN/v1.6/static/js/vendor.d7e01117.js'></script><script src='https://cdn.jsdelivr.net/gh/Baiyuetribe/kamifaka@CDN/v1.6/static/js/styles.61405570.js'></script><script src='https://cdn.jsdelivr.net/gh/Baiyuetribe/kamifaka@CDN/v1.6/static/js/app.eb72396d.js'></script></body></html>" > /usr/src/app/dist/index.html
# 自己fork后，上传自己的logo.png到项目service/system文件夹下
COPY service/system/logo.png /usr/src/app/service/system/logo.png

RUN sed -i 's|postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE}|$DATABASE_URL|g' docker-entrypoint.sh && \
    sed -i 's|8000|$PORT|g' docker-entrypoint.sh && \
    chmod +x docker-entrypoint.sh

EXPOSE $PORT

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
