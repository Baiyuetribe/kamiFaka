FROM alpine:3.10 as html-builder

RUN apk update && apk add brotli

RUN mkdir /html
COPY html/index.html /html

RUN gzip -9 -k /html/*html
RUN brotli -Z /html/*html


FROM nginx:1.17.9-alpine AS builder

ENV NGX_MODULE_COMMIT 0fdca2565dbedb88101ca19b1fb1511272f0821f
ENV NGX_MODULE_PATH ngx_brotli

RUN wget "http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -O nginx.tar.gz && \
  wget "https://github.com/google/ngx_brotli/archive/${NGX_MODULE_COMMIT}.tar.gz" -O ${NGX_MODULE_PATH}.tar.gz

# For latest build deps, see https://github.com/nginxinc/docker-nginx/blob/master/mainline/alpine/Dockerfile
RUN apk add --no-cache --virtual .build-deps \
  gcc \
  libc-dev \
  make \
  openssl-dev \
  pcre-dev \
  zlib-dev \
  linux-headers \
  libxslt-dev \
  gd-dev \
  geoip-dev \
  perl-dev \
  libedit-dev \
  mercurial \
  bash \
  alpine-sdk \
  findutils \
  brotli-dev

# Reuse same cli arguments as the nginx:alpine image used to build
RUN CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p') \
  tar -zxf nginx.tar.gz && \
  tar -xzf "${NGX_MODULE_PATH}.tar.gz" && \
  cd nginx-$NGINX_VERSION && \
  ./configure --with-compat $CONFARGS --add-dynamic-module="$(pwd)/../${NGX_MODULE_PATH}-${NGX_MODULE_COMMIT}" && \
  make && make install

# save /usr/lib/*so deps
RUN mkdir /so-deps && cp -L $(ldd /usr/local/nginx/modules/ngx_http_brotli_filter_module.so 2>/dev/null | grep '/usr/lib/' | awk '{ print $3 }' | tr '\n' ' ') /so-deps

FROM nginx:1.17.9-alpine

COPY --from=builder  /so-deps /usr/lib
COPY --from=builder  /usr/local/nginx/modules/ngx_http_brotli_filter_module.so /usr/local/nginx/modules/ngx_http_brotli_filter_module.so
COPY --from=builder  /usr/local/nginx/modules/ngx_http_brotli_static_module.so /usr/local/nginx/modules/ngx_http_brotli_static_module.so
COPY --chown=nginx:nginx dist /usr/share/nginx/html
COPY nginx /etc/nginx

# https://microbadger.com/images/lunaticcat/nginx-brotli
COPY Dockerfile /Dockerfile
LABEL org.label-schema.docker.dockerfile="/Dockerfile" \
  org.label-schema.vcs-type="Git" \
  org.label-schema.vcs-url="https://github.com/lunatic-cat/docker-nginx-brotli"

EXPOSE 80

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]

