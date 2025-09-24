# **mt_autologin**

使用 selenium 创建无头浏览器，通过模拟操作登录~~或通过登录凭证登录~~

支持通过[青龙面板](https://qinglong.online)或~~docker部署（开发中）~~

> 注意：需要科学上网

> 注意：仅建议将此脚本作为备用

> 注意：通过脚本登陆时会产生登录通知

> ~~注意：通过登录凭证登录时可能会产生“疑似登录凭证泄露”的通知~~

## 1. 通过青龙面板部署

### 1.1 下载脚本

下载mt_autologin文件夹

将mt_autologin文件夹上传至青龙面板

### 1.2 修改镜像源（可选）

Python软件包镜像源：https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

Linux软件包镜像源：https://mirrors.tuna.tsinghua.edu.cn

### 1.3 安装依赖

安装python依赖: selenium, pyotp, requests

安装linux依赖: chromium, chromium-chromedriver

### 1.4 设置环境变量

MT_USERNAME = your_mt_username

MT_PASSWORD = your_mt_password

MT_SECRET_KEY = your_mt_secret_key

DRIVER_PATH = your_driver_path

### 1.5 设置定时任务

## ~~2. 通过docker部署（开发中）~~