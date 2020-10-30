<p align="center">
  <a href="https://baiyue.one/">
    <img src="https://raw.githubusercontent.com/Baiyuetribe/baiyue_onekey/master/logo.png" alt="baiyue logo" width="90" height="90">
  </a>
</p>

<h1 align="center">佰阅发卡</h1>

<p align="center">
  基于VUE3.0+FLASK构建的全新卡密发卡系统
    <br>
  <br>
  <a href="https://jq.qq.com/?_wv=1027&k=1NdPevjF">反馈 bug</a>
  ·
  <a href="https://jq.qq.com/?_wv=1027&k=1NdPevjF">提交 功能</a>
  ·
  <a href="https://baiyue.one/">Blog</a>
</p>


## 预览地址：

最新版预览地址： http://107.148.243.178:994/#/
内测BUG反馈QQ群：853791822

## 部署方法：
环境准备：
```bash
# 程序需要Docker环境，如果不存在，则运行以下脚本。
echo y | bash <(curl -L -s https://raw.githubusercontent.com/Baiyuetribe/codes/master/docker.sh)
```
正式部署：
```bash
# 1.启动
## 1.1前端安装
docker run --name kmfaka-vue -itd --restart=always -p 999:80 baiyuetribe/kamifaka:bro1
## 1.2后端安装
docker run --name kmfaka-flask -itd --restart=always -p 5000:5000 baiyuetribe/kamifaka:flask
# 访问：https://您的IP地址:999  后台地址：#/admin    管理员账号：admin@qq.com 123456
## 2.卸载
docker rm -f kmfaka-vue kmfaka-flask
```



已完成数据库设计、后端api和前端UI设计，正在完成前后端对接和前端的相关业务逻辑。
访客页面：
![](home.png)
管理员界面：
![](dashboard.png)


## 内测说明
前端使用Ningx镜像，无特殊优化；后端使用Flask+sqlite做数据库。数据库可支持Mysql+Sqlite+postgresql等。为方便内测，数据暂未做本地缓存，卸载后一并删除。

功能概述:当前内测版已完成发卡系统的主要运行逻辑，前端的下单流程、后端的分类、商品、卡密、邮箱、通知信息等都非常完善。短信通知暂不可用外，其余都正常工作。

## 当前开发计划：
完善后端wsgi服务=》添加Docker服务=》上线预览版数据库=》发布第一个正式版

当前任务：征集内测bug



## 已完成功能：
访客界面：
- 商品展示首页
- 商品细节展示
- 订单查询
- 订单支付流程


管理员界面：
- 分类设置（增删改查）
- 商品设置（增删改查）
- 卡密设置（增删改查）
- 订单列表（查、删）
- 支付设置（核心模块）
- 消息通知
- 账户修改
- 邮箱设置

### 项目依赖
前端UI：Stisla --> https://github.com/stisla/stisla
前端交互程序：vue3.0 --> https://github.com/vuejs/vue-next
后端：Flask --> https://github.com/pallets/flask
管理员接口：Flask-JWT --> https://flask-jwt-extended.readthedocs.io/en/stable/

## 如何参与该开源项目？

我们欢迎任何人参进来，不论前端UI美化、细节讲究，还是代码BUG、功能异常等情况，都可以积极反馈。

## License

MIT