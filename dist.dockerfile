FROM nginx:stable-alpine
WORKDIR /usr/share/nginx/html
COPY dist /usr/share/nginx/html
EXPOSE 80
COPY entrypoint.sh .
ENTRYPOINT ["entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]