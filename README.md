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


## 预览地址：0.2版

最新版预览地址： http://107.148.243.178:8000

内测BUG反馈QQ群：853791822

## 部署方法：

一键部署：
```bash
docker run --name kmfaka -itd -p 8000:8000 baiyuetribe/kamifaka:0.2
```
然后访问http://您的ip:8000即可访问, 加上`/admin`跳转到管理员界面，默认账号：admin@qq.com 密码：123456

如需通过域名访问，请参考[宝塔如何设置域名反代任意端口？](https://baiyue.one/archives/527.html)

卸载命令：
```bash
docker rm -f kmfaka && docker rmi -f baiyuetribe/kamifaka:0.2
```


访客页面：
![](home.png)
管理员界面：
![](dashboard.png)


## 内测说明
当前还未发布正式版，内测主要征集各种BUG中，第一轮结束后。将发布第一个正式版。请做好反馈BUG的心态后再尝试本程序，否则请选择已经成熟的发卡系统。


## 当前开发计划：
收集BUG反馈=》发布第一个正式版

当前任务：征集内测bug

## 功能特色：

- Stisla UI：web界面很漂亮
- 前端使用VUE3.0,页面响应迅速
- 已集成支付宝当面付、码支付、Payjs、虎皮椒支付宝、虎皮椒微信
- 普通用户支持邮箱、短信接收消息
- 管理员支持邮箱、短信、TG、微信通知
- 支持批量导入卡密
- 商品可上下架


### 项目依赖
- 前端UI：Stisla --> https://github.com/stisla/stisla
- 前端交互程序：vue3.0 --> https://github.com/vuejs/vue-next
- 后端：Flask --> https://github.com/pallets/flask
- 管理员接口：Flask-JWT --> https://flask-jwt-extended.readthedocs.io/en/stable/

## 如何参与该开源项目？

我们欢迎任何人参进来，不论前端UI美化、细节讲究，还是代码BUG、功能异常等情况，欢迎积极反馈。内测BUG反馈QQ群：853791822

## License

MIT