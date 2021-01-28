<p align="center">
  <a href="https://github.com/Baiyuetribe/kamiFaka">
    <img src="https://cdn.jsdelivr.net/gh/Baiyuetribe/baiyue_onekey@master/logo.png" alt="baiyue logo" width="90" height="90">
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
  <a href="https://github.com/Baiyuetribe/kamiFaka/discussions">反馈 bug</a>
  ·
  <a href="https://kmfaka.baklib.com">教程 文档</a>
  ·
  <a href="https://baiyue.one/">Vlog</a>
</p>

海外DEMO演示1： http://107.148.243.178:8000

国内DEMO演示2： http://27.54.253.25:8000     [【该机器由茶猫云赞助,2天无理由全额退款】](https://zzzyun.com)             

默认管理员`admin@qq.com 123456`

## 适用场景：
适用于各种电商、优惠卷、论坛邀请码、充值卡、激活码、注册码、腾讯爱奇艺积分CDK等，支持手工和全自动发货，还有类似1688的分层批发模式。

## 功能特色：

- Stisla UI：web界面很漂亮
- 前端使用VUE3.0,毫秒级响应
- 已集成支付宝当面付、微信官方、Payjs、虎皮椒、YunGouOS、易支付、Mugglepay、码支付等十几种支付接口
- 普通用户支持邮箱、短信接收消息
- 管理员支持邮箱、短信、TG、微信、QQ通知
- 集成TG发卡系统
- 支持2~4层批发模式
- 长卡密可导出为txt文本
- 多种主题模式【列表、卡片、宫格】
- 支持自定义背景、标题、关键词等
- 支持热备份，可一键云端备份、一键导出备份文件到本地
- 数据库可分离，兼容Mysql、PostgreSQL和Sqlite
- 支持移动端唤醒支付宝
- JWT保证后台接口安全
- Limter保障服务器访问频率和次数


## 部署方法：

### 1. 正式环境【线上部署】
[如何使用宝塔面板Docker管理器一键部署佰阅发卡](https://baiyue.one/archives/1703.html)

[佰阅发卡KAMIFAKA：一款全新的基于VUE3.0+FLASK的卡密发卡系统](https://baiyue.one/archives/1700.html)

[视频安装教程：【从0开始一步步使用宝塔Docker管理器搭建佰阅发卡v1.3版【2020】](https://www.bilibili.com/video/BV1Ra4y1p7QS) 

[付费一键脚本： 全程无代码秒级部署](https://mall.baiyue.one/#/1/detail)

Github本地查看：[1.【宝塔+SQlite】](正式环境搭建教程.md#方法1宝塔nginxdocker数据库为sqlite)｜[2.【宝塔+Mysql】](正式环境搭建教程.md#方法2宝塔nginxdocker数据库为宝塔mysql)｜[3.【Heroku】](正式环境搭建教程.md#方法3heroku-无服务器部署)

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

### 3. 开发环境【如需修改或自定义，可查看该文档】

开发环境：[开发环境安装教程](开发环境安装教程.md)


访客页面：
![](https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/img/20/yyycode_comPc端演示.gif)
管理员界面：
![](https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/img/20/yyycode_comPc后台端演示.gif)

## Github社区讨论

项目已开通专属社区,主要集中开发者计划、BUG反馈、新功能建议等，欢迎积极参与讨论，[点此进入](https://github.com/Baiyuetribe/kamiFaka/discussions) 

### 项目依赖
- 前端UI：Stisla --> https://github.com/stisla/stisla
- 前端交互程序：vue3.0 --> https://github.com/vuejs/vue-next
- 后端：Flask --> https://github.com/pallets/flask
- 管理员接口：Flask-JWT --> https://flask-jwt-extended.readthedocs.io/en/stable/

## 如何参与该开源项目？

[查看可参与的任务](查看可参与的任务.md)

项目交流QQ群：853791822

官方帮助文档：[https://kmfaka.baklib.com](https://kmfaka.baklib.com)

## License

本程序使用MIT协议，您可以免费使用，复制或修改软件，但是请保留底部作者信息和License许可声明。
