FROM baiyuetribe/kamifaka:bro_base

COPY --chown=nginx:nginx dist /usr/share/nginx/html

EXPOSE 80
STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]