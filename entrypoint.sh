#!/bin/bash
#解决服务器端ip地址固定的bug
ip=$(curl -4 ip.sb)
cd /usr/share/nginx/html/js
file=`ls *.js`;
echo $file
for item in $file
do
    filename=${item%.*}
    echo $filename
    sed -i "s/127.0.0.1/'$ip'/g" $item
done
# ip=1.1.1.1
# sed -i "s/127.0.0.1/'$ip'/g" test.js

echo Serving application

nginx -g 'daemon off