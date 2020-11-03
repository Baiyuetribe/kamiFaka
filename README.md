<p align="center">
  <a href="https://baiyue.one/">
    <img src="https://raw.githubusercontent.com/Baiyuetribe/baiyue_onekey/master/logo.png" alt="baiyue logo" width="90" height="90">
  </a>
</p>

<h1 align="center">佰阅发卡</h1>

<p align="center">
  基于VUE3.0+FLASK构建的全新卡密发卡系统
    <br>
    <img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/Baiyuetribe/kamiFaka/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%9E%84%E5%BB%BADocker%E9%95%9C%E5%83%8F/master?label=Docker&style=for-the-badge">
    <img alt="Docker Image Size (latest semver)" src="https://img.shields.io/docker/image-size/baiyuetribe/kamifaka?style=for-the-badge">
    <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/baiyuetribe/kamifaka?style=for-the-badge">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/baiyuetribe/kamifaka?style=for-the-badge">

  <br>
  <a href="https://jq.qq.com/?_wv=1027&k=1NdPevjF">反馈 bug</a>
  ·
  <a href="https://jq.qq.com/?_wv=1027&k=1NdPevjF">提交 功能</a>
  ·
  <a href="https://baiyue.one/">Blog</a>
</p>

最新版预览地址： http://107.148.243.178:8000

内测BUG反馈QQ群：853791822

## 部署方法：

正式环境（线上环境）教程：[佰阅发卡KAMIFAKA：一款全新的基于VUE3.0+FLASK的卡密发卡系统](https://baiyue.one/archives/1700.html)


一键部署：
```bash
docker run --name kmfaka -itd -p 8000:8000 baiyuetribe/kamifaka:latest
```
然后访问http://您的ip:8000即可访问, 加上`/admin`跳转到管理员界面，默认账号：admin@qq.com 密码：123456

如需通过域名访问，请参考[宝塔如何设置域名反代任意端口？](https://baiyue.one/archives/527.html)

卸载命令：
```bash
docker rm -f kmfaka && docker rmi -f baiyuetribe/kamifaka:latest
```
【国内环境】：阿里云镜像加速【适合国内服务器或本地使用】：
```bash
docker run --name kmfaka -itd -p 8000:8000 registry.cn-hangzhou.aliyuncs.com/baiyuetribe/kamifaka:latest
```
【国内环境】：卸载命令：
```bash
docker rm -f kmfaka && docker rmi -f registry.cn-hangzhou.aliyuncs.com/baiyuetribe/kamifaka:latest
```


访客页面：
![](https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/img/20/yyycode_comPc端演示.gif)
管理员界面：
![](https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/img/20/yyycode_comPc后台端演示.gif)

## 当前开发计划：
发布第一个正式版-->撰写帮助文档

当前任务：征集内测bug、写操作文档

## 功能特色：

- Stisla UI：web界面很漂亮
- 前端使用VUE3.0,页面响应迅速
- 已集成支付宝当面付、码支付、Payjs、虎皮椒支付宝、虎皮椒微信
- 普通用户支持邮箱、短信接收消息
- 管理员支持邮箱、短信、TG、微信通知
- 支持批量导入卡密
- 商品可上下架
- 支持自定义背景


### 项目依赖
- 前端UI：Stisla --> https://github.com/stisla/stisla
- 前端交互程序：vue3.0 --> https://github.com/vuejs/vue-next
- 后端：Flask --> https://github.com/pallets/flask
- 管理员接口：Flask-JWT --> https://flask-jwt-extended.readthedocs.io/en/stable/

## 如何参与该开源项目？

我们欢迎任何人参进来，不论前端UI美化、细节讲究，还是代码BUG、功能异常等情况，欢迎积极反馈。内测BUG反馈QQ群：853791822

## License

MIT