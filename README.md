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

### 1. 正式环境【线上部署】
[如何使用宝塔面板Docker管理器一键部署佰阅发卡](https://baiyue.one/archives/1703.html)

[佰阅发卡KAMIFAKA：一款全新的基于VUE3.0+FLASK的卡密发卡系统](https://baiyue.one/archives/1700.html)

Github本地查看：[1.【宝塔+SQlite】 2.【宝塔+Mysql】](正式环境搭建教程.md)

### 2. 线上快速体验
Heroku 一键部署：[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https%3A%2F%2Fgithub.com%2FBaiyuetribe%2FkamiFaka)

PWD 一键部署：[![Try in PWD](https://cdn.rawgit.com/play-with-docker/stacks/cff22438/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/Baiyuetribe/kamiFaka/master/pwd.yml)

个人服务器快速安装：
```bash
# 安装命令
docker run --name kmfaka -itd -p 8000:8000 baiyuetribe/kamifaka:latest
```
```bash
# 卸载命令
docker rm -f kmfaka && docker rmi -f baiyuetribe/kamifaka:latest
```

### 3. 开发环境

开发环境：[开发环境安装教程](开发环境安装教程.md)


访客页面：
![](https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/img/20/yyycode_comPc端演示.gif)
管理员界面：
![](https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/img/20/yyycode_comPc后台端演示.gif)

## 当前开发计划：
发布第一个正式版-->撰写帮助文档

当前任务：操作文档、富文本编辑器、

## 功能特色：

- Stisla UI：web界面很漂亮
- 前端使用VUE3.0,页面响应迅速
- 已集成支付宝当面付、码支付、Payjs、虎皮椒支付宝、虎皮椒微信
- 普通用户支持邮箱、短信接收消息
- 管理员支持邮箱、短信、TG、微信通知
- 支持批量导入卡密
- 商品可上下架
- 支持自定义背景
- 支持网站配置备份、热更新
- 数据库可分离，兼容Sqlite和Mysql


### 项目依赖
- 前端UI：Stisla --> https://github.com/stisla/stisla
- 前端交互程序：vue3.0 --> https://github.com/vuejs/vue-next
- 后端：Flask --> https://github.com/pallets/flask
- 管理员接口：Flask-JWT --> https://flask-jwt-extended.readthedocs.io/en/stable/

## 如何参与该开源项目？

[查看可参与的任务](查看可参与的任务.md)
内测BUG反馈QQ群：853791822

## License

本程序使用MIT协议，您可以免费使用，复制或修改软件，但是请保留底部作者信息和License许可声明。
